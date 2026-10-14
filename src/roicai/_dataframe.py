# Hand-written: scripts/patch_generated.py adds these mixins to the generated
# models and pagers, so every response has to_pandas() and to_polars().

from __future__ import annotations

import datetime as dt
import types
import typing
import warnings

if typing.TYPE_CHECKING:
    import pandas
    import polars

# Columns left out of every frame: `object` names the resource type, which is
# the same on every row.
SKIPPED_COLUMNS = frozenset({"object"})

DEFAULT_MAX_ITEMS = 10_000


def _import(module: str) -> typing.Any:
    try:
        return __import__(module)
    except ImportError:
        raise ImportError(f'to_{module}() needs {module}. Install it with: pip install "roicai[{module}]"') from None


def _unwrap(annotation: typing.Any) -> typing.Any:
    """Returns the type a field holds without Optional, or None for a mixed union."""
    origin = typing.get_origin(annotation)
    if origin is typing.Union or origin is types.UnionType:
        args = [a for a in typing.get_args(annotation) if a is not type(None)]
        literals = [a for a in args if typing.get_origin(a) is typing.Literal]
        # Fern types an open enum as Union[Literal[...], Any].
        if literals and all(a is typing.Any or a in literals for a in args):
            return str
        return _unwrap(args[0]) if len(args) == 1 else None
    if origin is typing.Literal:
        values = typing.get_args(annotation)
        return str if all(isinstance(v, str) for v in values) else None
    if typing.get_origin(annotation) is typing.Annotated:
        return _unwrap(typing.get_args(annotation)[0])
    return annotation


def _row_model(model: typing.Any) -> typing.Any:
    """Returns the model class of the rows `model` holds: its `data` items, or itself."""
    fields = getattr(type(model), "model_fields", {})
    if "data" in fields:
        annotation = _unwrap(fields["data"].annotation)
        if typing.get_origin(annotation) in (list, typing.List):
            (item,) = typing.get_args(annotation)
            return item
    return type(model)


def _rows(model: typing.Any) -> list:
    fields = getattr(type(model), "model_fields", {})
    if "data" in fields and isinstance(getattr(model, "data", None), list):
        return list(model.data)
    return [model]


def _columns(row_model: typing.Any) -> dict[str, typing.Any]:
    """Maps each column name to the scalar type its values have, or None."""
    columns: dict[str, typing.Any] = {}
    for name, field in getattr(row_model, "model_fields", {}).items():
        column = field.alias or name
        if column not in SKIPPED_COLUMNS:
            columns[column] = _unwrap(field.annotation)
    return columns


def _records(items: typing.Iterable[typing.Any]) -> list[dict]:
    records = []
    for item in items:
        record = item.model_dump(by_alias=True) if hasattr(item, "model_dump") else dict(item)
        for column in SKIPPED_COLUMNS:
            record.pop(column, None)
        records.append(record)
    return records


def build_pandas(items: list, row_model: typing.Any) -> pandas.DataFrame:
    pd = _import("pandas")
    columns = _columns(row_model)
    records = _records(items)
    names = list(columns) + [c for r in records for c in r if c not in columns]
    frame = pd.DataFrame.from_records(records, columns=list(dict.fromkeys(names)))
    for column, kind in columns.items():
        if kind is bool:
            frame[column] = frame[column].astype("boolean")
        elif kind is int:
            frame[column] = frame[column].astype("Int64")
        elif kind is float:
            frame[column] = frame[column].astype("float64")
        elif kind is dt.datetime:
            frame[column] = pd.to_datetime(frame[column], utc=True)
        elif kind is dt.date:
            frame[column] = pd.to_datetime(frame[column])
    return frame


def build_polars(items: list, row_model: typing.Any) -> polars.DataFrame:
    pl = _import("polars")
    kinds = {
        bool: pl.Boolean,
        int: pl.Int64,
        float: pl.Float64,
        str: pl.String,
        dt.date: pl.Date,
        dt.datetime: pl.Datetime("us", "UTC"),
    }
    columns = _columns(row_model)
    records = _records(items)
    schema = {c: kinds.get(k) for c, k in columns.items()}
    if not records:
        return pl.DataFrame(schema={c: t or pl.Null for c, t in schema.items()})
    overrides = {c: t for c, t in schema.items() if t is not None}
    frame = pl.DataFrame(records, schema_overrides=overrides, infer_schema_length=None, strict=False)
    order = [c for c in columns if c in frame.columns]
    return frame.select(order + [c for c in frame.columns if c not in columns])


def _collect(pager: typing.Any, max_items: typing.Optional[int]) -> list:
    _check(max_items)
    items: list[typing.Any] = []
    for page in pager.iter_pages():
        if _take(items, page, max_items):
            break
    return items


async def _acollect(pager: typing.Any, max_items: typing.Optional[int]) -> list:
    _check(max_items)
    items: list[typing.Any] = []
    async for page in pager.iter_pages():
        if _take(items, page, max_items):
            break
    return items


def _take(items: list, page: typing.Any, max_items: typing.Optional[int]) -> bool:
    """Adds a page's items to `items`; returns True when max_items is reached.

    Decides whether rows remain from the page itself, so reaching max_items at
    the end of a page doesn't request the next page only to find out.
    """
    page_items = page.items or []
    if max_items is None:
        items.extend(page_items)
        return False
    room = max_items - len(items)
    items.extend(page_items[:room])
    if len(items) < max_items:
        return False
    if len(page_items) > room or page.has_next:
        _warn_truncated(max_items)
    return True


def _check(max_items: typing.Optional[int]) -> None:
    if max_items is not None and (not isinstance(max_items, int) or isinstance(max_items, bool) or max_items < 1):
        raise ValueError("max_items must be a positive integer, or None for no limit")


def _warn_truncated(max_items: int) -> None:
    warnings.warn(
        f"Stopped after max_items={max_items} rows; more pages remain. "
        "Pass a larger max_items, or max_items=None to fetch every page.",
        stacklevel=5,
    )


class ModelFrameMixin:
    """DataFrame conversion for responses: a list's rows, or one object as one row."""

    def to_pandas(self) -> pandas.DataFrame:
        """Returns this response as a pandas DataFrame.

        A list becomes one row per item and anything else one row. Columns are
        the API's field names, in its order. Dates and times are datetime64
        columns, and whole numbers that can be null are nullable `Int64`.
        Needs pandas: pip install "roicai[pandas]".
        """
        return build_pandas(_rows(self), _row_model(self))

    def to_polars(self) -> polars.DataFrame:
        """Returns this response as a polars DataFrame, typed from the API's schema.

        Needs polars: pip install "roicai[polars]".
        """
        return build_polars(_rows(self), _row_model(self))


class SyncPagerFrameMixin:
    """DataFrame conversion for list methods, fetching later pages as needed."""

    def to_pandas(self, *, max_items: typing.Optional[int] = DEFAULT_MAX_ITEMS) -> pandas.DataFrame:
        """Returns the items of this page and the pages after it as a pandas DataFrame.

        Fetches pages until the list ends or `max_items` items are in hand,
        warning if it stops early. Pass `max_items=None` for no limit: every
        page is one request. Needs pandas: pip install "roicai[pandas]".
        """
        _import("pandas")
        return build_pandas(_collect(self, max_items), _row_model(self.response))  # type: ignore[attr-defined]

    def to_polars(self, *, max_items: typing.Optional[int] = DEFAULT_MAX_ITEMS) -> polars.DataFrame:
        """Returns the items of this page and the pages after it as a polars DataFrame.

        Fetches pages like to_pandas(). Needs polars: pip install "roicai[polars]".
        """
        _import("polars")
        return build_polars(_collect(self, max_items), _row_model(self.response))  # type: ignore[attr-defined]


class AsyncPagerFrameMixin:
    """DataFrame conversion for async list methods, fetching later pages as needed."""

    async def to_pandas(self, *, max_items: typing.Optional[int] = DEFAULT_MAX_ITEMS) -> pandas.DataFrame:
        """Returns the items of this page and the pages after it as a pandas DataFrame.

        Fetches pages until the list ends or `max_items` items are in hand,
        warning if it stops early. Pass `max_items=None` for no limit: every
        page is one request. Needs pandas: pip install "roicai[pandas]".
        """
        _import("pandas")
        return build_pandas(await _acollect(self, max_items), _row_model(self.response))  # type: ignore[attr-defined]

    async def to_polars(self, *, max_items: typing.Optional[int] = DEFAULT_MAX_ITEMS) -> polars.DataFrame:
        """Returns the items of this page and the pages after it as a polars DataFrame.

        Fetches pages like to_pandas(). Needs polars: pip install "roicai[polars]".
        """
        _import("polars")
        return build_polars(await _acollect(self, max_items), _row_model(self.response))  # type: ignore[attr-defined]
