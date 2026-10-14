"""Applies the SDK's changes to the code Fern generated.

    python scripts/patch_generated.py build/generated

Each change replaces text Fern is known to write and fails if it is missing,
so a Fern upgrade that changes it stops generation rather than silently
dropping the change:

- Requests send a User-Agent of roicai-python/<version>, with the client's
  app_info appended. Fern sends none when it generates locally.
- List methods request the next page with the `page` token of
  `next_page_url` (see src/roicai/_paging.py).
- Models and pagers get to_pandas() and to_polars() (src/roicai/_dataframe.py).
- Errors have the fields of the API's error body (`message`, `code`,
  `request_id`...) and a message that leads with them
  (src/roicai/_errors.py), rather than every response header.
- A client without an API key says how to give it one.
- The SDK logs to the `roicai` logger, not `fern`.
- `next_page()` returns None on the last page, rather than requesting the
  first page again.
- Streamed responses, such as logos, are retried like other requests.
- `model_dump()` and `model_dump_json()` honour `include` and `exclude` (Fern's
  JSON serializer is removed).
- `AsyncRoicai(async_token=...)` needs no API key as well, and an empty API
  key gets the same message as a missing one.
- The clients can be closed: `close()` or `with Roicai() as client`, and
  `aclose()` or `async with AsyncRoicai() as client`.
- `client.tickers` and every other group property is annotated, so mypy
  checks calls through them rather than reading them as Any.
- Path parameters are percent-encoded, so a value with "/", "?" or "#" stays
  in its path segment.
- An error response whose body isn't the API's JSON error, such as a proxy's
  HTML page, still raises the error class for its status
  (`error_body` in src/roicai/_errors.py).
- Importing the package adds no log handler; one is added only when the
  client's `logging` option turns messages on.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

MISSING_KEY = '"The client must be instantiated be either passing in api_key or setting ROICAI_API_KEY"'
MISSING_KEY_FIX = (
    '"No API key: pass api_key to the client, or set the ROICAI_API_KEY environment variable. '
    'Get a key at https://www.roic.ai/api"'
)
API_ERROR_STR = """
    def __str__(self) -> str:
        return f"headers: {self.headers}, status_code: {self.status_code}, body: {self.body}"
"""

NEXT_PAGE = (
    "        return self.get_next() if self.get_next is not None else None\n",
    "        if not self.has_next or self.get_next is None:\n            return None\n        return self.get_next()\n",
)
ASYNC_NEXT_PAGE = (
    "        return await self.get_next() if self.get_next is not None else None\n",
    "        if not self.has_next or self.get_next is None:\n            return None\n        return await self.get_next()\n",
)

# Fern retries request() but not stream(). Each stream() retries the same way:
# on a retryable status it closes the response, waits, and opens a new one.
STREAM_RETRY = """
            _max_retries = (
                request_options.get("max_retries", self.base_max_retries)
                if request_options is not None
                else self.base_max_retries
            )
            if not (_should_retry(response=stream) and retries < _max_retries):
                yield stream
                return
            _delay = _retry_timeout(response=stream, retries=retries)
        {sleep}
        {with_} self.stream(
            path,
            method=method,
            base_url=base_url,
            params=params,
            json=json,
            data=data,
            content=content,
            files=files,
            headers=headers,
            request_options=request_options,
            retries=retries + 1,
            omit=omit,
            optional_body=optional_body,
            force_multipart=force_multipart,
        ) as stream:
            yield stream
"""
STREAM_END = "        ) as stream:\n            yield stream\n"

# Fern's JSON serializer ignores include and exclude in model_dump_json(), and
# with pydantic before 2.14 its presence makes model_dump() ignore them too.
# Without it, pydantic's own serialization applies: the same field names, since
# the models have no aliases, with timestamps in ISO 8601.
SERIALIZE = (
    """        @pydantic.model_serializer(mode="plain", when_used="json")  # type: ignore[attr-defined]
        def serialize_model(self) -> Any:  # type: ignore[name-defined]
            serialized = self.dict()  # type: ignore[attr-defined]
            data = {k: serialize_datetime(v) if isinstance(v, dt.datetime) else v for k, v in serialized.items()}
            return data

""",
    "",
)


def main(root: Path) -> None:
    patch(
        root / "core/client_wrapper.py",
        (
            "            **(self.get_custom_headers() or {}),\n",
            '            "User-Agent": _append_app_info_to_user_agent(USER_AGENT, self._app_info),\n'
            "            **(self.get_custom_headers() or {}),\n",
        ),
        imports="from .._version import USER_AGENT",
    )
    patch(
        root / "core/pagination.py",
        ("class SyncPager(Generic[T, R]):", "class SyncPager(SyncPagerFrameMixin, Generic[T, R]):"),
        ("class AsyncPager(Generic[T, R]):", "class AsyncPager(AsyncPagerFrameMixin, Generic[T, R]):"),
        NEXT_PAGE,
        ASYNC_NEXT_PAGE,
        imports="from .._dataframe import AsyncPagerFrameMixin, SyncPagerFrameMixin",
    )
    patch(
        root / "core/pydantic_utilities.py",
        (
            "class UniversalBaseModel(pydantic.BaseModel):",
            "class UniversalBaseModel(ModelFrameMixin, pydantic.BaseModel):",
        ),
        SERIALIZE,
        imports="from .._dataframe import ModelFrameMixin",
    )
    patch(
        root / "core/api_error.py",
        ("class ApiError(Exception):", "class ApiError(ApiErrorDetailsMixin, Exception):"),
        (API_ERROR_STR, ""),
        imports="from .._errors import ApiErrorDetailsMixin",
    )
    patch(root / "client.py", (MISSING_KEY, MISSING_KEY_FIX), count=2)
    patch_async_token(root / "client.py")
    patch(root / "client.py", ("        if api_key is None:\n", "        if not api_key:\n"))
    patch(
        root / "client.py",
        (
            "        self._fundamentals: typing.Optional[FundamentalsClient] = None\n",
            "        self._fundamentals: typing.Optional[FundamentalsClient] = None\n" + SYNC_CLOSE,
        ),
        (
            "        self._fundamentals: typing.Optional[AsyncFundamentalsClient] = None\n",
            "        self._fundamentals: typing.Optional[AsyncFundamentalsClient] = None\n" + ASYNC_CLOSE,
        ),
    )
    # mypy reads an unannotated property as Any, so `client.tickers` and every
    # call through it would go unchecked.
    annotated = sum(regex_patch(path, GROUP_PROPERTY, r"def \1(self) -> \3:\n\2") for path in root.rglob("client.py"))
    if annotated < 40:
        sys.exit(f"patch_generated: annotated only {annotated} group properties; did their code change?")
    patch_streams(root / "core/http_client.py")
    patch(
        root / "core/logging.py",
        ('logging.getLogger("fern")', 'logging.getLogger("roicai")'),
        (
            '_default_logger: Logger = Logger(level="info", logger=ConsoleLogger(), silent=True)',
            "# Silent, so it never logs: a ConsoleLogger would add a handler on import.\n"
            '_default_logger: Logger = Logger(level="info", logger=typing.cast(ILogger, logging.getLogger("roicai")), silent=True)',
        ),
    )

    for path in root.rglob("raw_client.py"):
        dots = "." * len(path.relative_to(root).parts)
        text = path.read_text()
        if "encode_path_param(" in text:
            patch(path, ("encode_path_param(", "quote_path_param("), count=None)
            patch(path, ("import encode_path_param", "import quote_path_param"))
        if "type_=Error," in text:
            if not regex_patch(path, ERROR_BODY, "body=error_body(_response),"):
                sys.exit(f"patch_generated: expected the error bodies in {path} to parse type_=Error")
            patch(path, imports=f"from {dots}_errors import error_body")

    paged = [p for p in root.rglob("raw_client.py") if "_parsed_next = _parsed_response.next_page_url" in p.read_text()]
    if not paged:
        sys.exit("patch_generated: no list method reads next_page_url; did the pagination settings change?")
    for path in paged:
        dots = "." * len(path.relative_to(root).parts)
        patch(
            path,
            (
                "_parsed_next = _parsed_response.next_page_url",
                "_parsed_next = page_token(_parsed_response.next_page_url)",
            ),
            imports=f"from {dots}_paging import page_token",
            count=None,
        )


GROUP_PROPERTY = re.compile(r"def (\w+)\(self\):\n(        if self\._\1 is None:\n            from \S+ import (\w+))")
ERROR_BODY = re.compile(
    r"body=typing\.cast\(\s*Error,\s*parse_obj_as\(\s*type_=Error,\s*# type: ignore\s*"
    r"object_=_response\.json\(\),\s*\),\s*\),"
)
SYNC_CLOSE = """
    def close(self) -> None:
        \"\"\"Closes the HTTP client and its connections.\"\"\"
        self._client_wrapper.httpx_client.httpx_client.close()

    def __enter__(self) -> "Roicai":
        return self

    def __exit__(self, *exc_info: typing.Any) -> None:
        self.close()
"""
ASYNC_CLOSE = """
    async def aclose(self) -> None:
        \"\"\"Closes the HTTP client and its connections.\"\"\"
        await self._client_wrapper.httpx_client.httpx_client.aclose()

    async def __aenter__(self) -> "AsyncRoicai":
        return self

    async def __aexit__(self, *exc_info: typing.Any) -> None:
        await self.aclose()
"""


def regex_patch(path: Path, pattern: re.Pattern, repl: str) -> int:
    text, found = pattern.subn(repl, path.read_text())
    path.write_text(text)
    return found


def patch_streams(path: Path) -> None:
    text = path.read_text()
    sync_part, separator, async_part = text.partition("class AsyncHttpClient:")
    if not separator or sync_part.count(STREAM_END) != 1 or async_part.count(STREAM_END) != 1:
        sys.exit(f"patch_generated: expected one stream() ending in each client of {path}")
    sync_part = sync_part.replace(
        STREAM_END, "        ) as stream:" + STREAM_RETRY.format(sleep="time.sleep(_delay)", with_="with")
    )
    async_part = async_part.replace(
        STREAM_END,
        "        ) as stream:" + STREAM_RETRY.format(sleep="await asyncio.sleep(_delay)", with_="async with"),
    )
    path.write_text(sync_part + separator + async_part)


def patch_async_token(path: Path) -> None:
    """Lets AsyncRoicai take async_token without api_key, as the wrapper allows."""
    text = path.read_text()
    sync_part, separator, async_part = text.partition("class AsyncRoicai:")
    check = "        if api_key is None:\n"
    passed = "            api_key=api_key,\n"
    if not separator or async_part.count(check) != 1 or async_part.count(passed) != 1:
        sys.exit(f"patch_generated: expected one API key check in AsyncRoicai in {path}")
    async_part = async_part.replace(check, "        if not api_key and async_token is None:\n")
    # With async_token, the wrapper sends the token and never the key.
    async_part = async_part.replace(passed, '            api_key=api_key or "",\n')
    path.write_text(sync_part + separator + async_part)


def patch(path: Path, *replacements: tuple[str, str], imports: str | None = None, count: int | None = 1) -> None:
    text = path.read_text()
    for old, new in replacements:
        found = text.count(old)
        if found == 0 or (count is not None and found != count):
            sys.exit(f"patch_generated: expected {count or 'some'} of {old!r} in {path}, found {found}")
        text = text.replace(old, new)
    if imports:
        lines = text.splitlines(keepends=True)
        # After the header comment and any `from __future__` import.
        at = 0
        while at < len(lines) and (
            lines[at].startswith("#") or not lines[at].strip() or lines[at].startswith("from __future__")
        ):
            at += 1
        lines.insert(at, imports + "\n")
        text = "".join(lines)
    path.write_text(text)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(Path(sys.argv[1]))
