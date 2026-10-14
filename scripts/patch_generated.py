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
"""

from __future__ import annotations

import sys
from pathlib import Path

MISSING_KEY = '"The client must be instantiated be either passing in api_key or setting ROICAI_API_KEY"'
MISSING_KEY_FIX = (
    '"No API key: pass api_key to the client, or set the ROICAI_API_KEY environment variable. '
    'Get a key at https://roic.ai/api"'
)
API_ERROR_STR = """
    def __str__(self) -> str:
        return f"headers: {self.headers}, status_code: {self.status_code}, body: {self.body}"
"""


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
        imports="from .._dataframe import AsyncPagerFrameMixin, SyncPagerFrameMixin",
    )
    patch(
        root / "core/pydantic_utilities.py",
        (
            "class UniversalBaseModel(pydantic.BaseModel):",
            "class UniversalBaseModel(ModelFrameMixin, pydantic.BaseModel):",
        ),
        imports="from .._dataframe import ModelFrameMixin",
    )
    patch(
        root / "core/api_error.py",
        ("class ApiError(Exception):", "class ApiError(ApiErrorDetailsMixin, Exception):"),
        (API_ERROR_STR, ""),
        imports="from .._errors import ApiErrorDetailsMixin",
    )
    patch(root / "client.py", (MISSING_KEY, MISSING_KEY_FIX), count=2)
    patch(root / "core/logging.py", ('logging.getLogger("fern")', 'logging.getLogger("roicai")'))

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
