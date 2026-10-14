# Hand-written: scripts/patch_generated.py makes ApiError, the base class of
# every error the API returns, inherit this.

from __future__ import annotations

import typing
from json import JSONDecodeError

import pydantic

if typing.TYPE_CHECKING:
    import httpx


def error_body(response: httpx.Response) -> typing.Any:
    """The body of an error response: the API's Error model, or the raw JSON or text.

    A response from a proxy, such as an HTML error page, still raises the
    error class for its status, with the page as its body.
    """
    from .core.pydantic_utilities import parse_obj_as
    from .types.error import Error

    try:
        data = response.json()
    except JSONDecodeError:
        return response.text
    try:
        return parse_obj_as(Error, data)
    except pydantic.ValidationError:
        return data


def _rebuild(cls: type, state: dict) -> typing.Any:
    error = cls.__new__(cls)  # type: ignore[call-overload]
    error.__dict__.update(state)
    return error


class ApiErrorDetailsMixin:
    """The fields of the API's error body, and a message that leads with them."""

    status_code: typing.Optional[int]
    body: typing.Any

    def _detail(self, name: str) -> typing.Optional[str]:
        error = getattr(self.body, "error", None)
        if error is None and isinstance(self.body, dict):
            error = self.body.get("error")
        if isinstance(error, dict):
            return error.get(name)
        return getattr(error, name, None)

    @property
    def message(self) -> typing.Optional[str]:
        """What went wrong, in a sentence."""
        return self._detail("message")

    @property
    def type(self) -> typing.Optional[str]:
        """The kind of error, such as `invalid_request_error`."""
        return self._detail("type")

    @property
    def code(self) -> typing.Optional[str]:
        """A short string for the error, such as `resource_missing`."""
        return self._detail("code")

    @property
    def param(self) -> typing.Optional[str]:
        """The parameter the error is about, if it is about one."""
        return self._detail("param")

    @property
    def request_id(self) -> typing.Optional[str]:
        """The ID of the request, to quote to support."""
        return self._detail("request_id")

    def __reduce__(self) -> typing.Any:
        # The generated subclasses take different __init__ arguments, so they
        # are rebuilt from their attributes, for pickle, copy and multiprocessing.
        return (_rebuild, (type(self), dict(self.__dict__)))

    def __repr__(self) -> str:
        if self.status_code is None:
            return f"{type(self).__name__}({self.body!r})"
        return (
            f"{type(self).__name__}(status_code={self.status_code}, message={self.message!r}, "
            f"code={self.code!r}, request_id={self.request_id!r})"
        )

    def __str__(self) -> str:
        message = self.message
        if self.status_code is None:
            # Raised before any request, such as for a missing API key.
            return str(self.body)
        if message is None:
            return f"HTTP {self.status_code}: {self.body!r}"
        details = ", ".join(f"{k}: {v}" for k, v in (("code", self.code), ("request_id", self.request_id)) if v)
        return f"HTTP {self.status_code}: {message}" + (f" ({details})" if details else "")
