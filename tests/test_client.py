"""Offline tests of the hand-written behaviour, with the HTTP layer mocked."""

from __future__ import annotations

import datetime as dt
import sys
import warnings
from urllib.parse import parse_qs, urlsplit

import httpx
import pytest
import respx

from roicai import ApiError, AsyncRoicai, NotFoundError, Roicai, TooManyRequestsError, __version__
from roicai._paging import page_token

BASE = "https://api.roic.ai"
STATEMENTS = f"{BASE}/v3.0.0/fundamental/income-statement/NASDAQ:AAPL"


def statement(year: int, **fields: object) -> dict:
    return {
        "id": f"fnd_{year}",
        "object": "v3.fundamentals.income_statement",
        "symbol": "NASDAQ:AAPL",
        "period_type": "annual",
        "period_end_date": f"{year}-09-30",
        "fiscal_year": year,
        "period_label": "FY",
        "currency": "USD",
        "price_currency": "USD",
        "fx_applied": False,
        "is_net_income": 1000.5 * year,
        **fields,
    }


def page(rows: list, next_token: str | None = None) -> dict:
    url = f"/v3.0.0/fundamental/income-statement/NASDAQ:AAPL?page={next_token}" if next_token else None
    return {"data": rows, "next_page_url": url, "previous_page_url": None}


def error(status: int, code: str) -> httpx.Response:
    body = {
        "error": {
            "type": "invalid_request_error",
            "code": code,
            "message": "Something went wrong.",
            "param": None,
            "doc_url": None,
            "request_id": "req_123",
        }
    }
    return httpx.Response(status, json=body)


def query(request: httpx.Request) -> dict:
    return {k: v[0] for k, v in parse_qs(urlsplit(str(request.url)).query).items()}


@pytest.fixture
def client() -> Roicai:
    return Roicai(api_key="test_key", max_retries=0)


@pytest.fixture
def async_client() -> AsyncRoicai:
    # An explicit httpx client, which respx mocks: with the aiohttp extra
    # installed, the default would be aiohttp.
    return AsyncRoicai(api_key="test_key", max_retries=0, httpx_client=httpx.AsyncClient())


def test_page_token() -> None:
    assert page_token("/v3.0.0/tickers?limit=2&page=page_v1_abc") == "page_v1_abc"
    assert page_token("https://api.roic.ai/v3.0.0/tickers?page=a%2Bb") == "a+b"
    assert page_token("/v3.0.0/tickers?limit=2") is None
    assert page_token(None) is None
    assert page_token("") is None


@respx.mock
def test_next_page_resends_the_request_with_the_token(client: Roicai) -> None:
    route = respx.get(STATEMENTS).mock(
        side_effect=[
            httpx.Response(200, json=page([statement(2025), statement(2024)], "tok2")),
            httpx.Response(200, json=page([statement(2023)])),
        ]
    )
    pager = client.fundamentals.income_statements.list(
        "NASDAQ:AAPL", period_type="annual", fiscal_year_gte=2015, date_lt="2026-01-01", limit=2
    )
    assert [r.fiscal_year for r in pager] == [2025, 2024, 2023]

    first, second = (query(call.request) for call in route.calls)
    assert first == {"period_type": "annual", "fiscal_year.gte": "2015", "date.lt": "2026-01-01", "limit": "2"}
    assert second == {**first, "page": "tok2"}


@respx.mock
def test_an_error_on_a_later_page_raises_its_error(client: Roicai) -> None:
    respx.get(STATEMENTS).mock(
        side_effect=[httpx.Response(200, json=page([statement(2025)], "tok2")), error(429, "rate_limited")]
    )
    with pytest.raises(TooManyRequestsError) as raised:
        list(client.fundamentals.income_statements.list("NASDAQ:AAPL"))
    assert raised.value.code == "rate_limited"


@respx.mock
def test_requests_send_the_key_and_user_agent() -> None:
    route = respx.get(STATEMENTS).mock(return_value=httpx.Response(200, json=page([])))
    client = Roicai(api_key="test_key", app_info={"name": "my-app", "version": "1.0"})
    client.fundamentals.income_statements.list("NASDAQ:AAPL")
    headers = route.calls.last.request.headers
    assert headers["authorization"] == "Bearer test_key"
    assert headers["user-agent"] == f"roicai-python/{__version__} my-app/1.0"
    assert "apikey" not in str(route.calls.last.request.url)


def test_the_key_comes_from_the_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ROICAI_API_KEY", "env_key")
    assert Roicai()._client_wrapper.get_headers()["Authorization"] == "Bearer env_key"
    monkeypatch.delenv("ROICAI_API_KEY")
    with pytest.raises(ApiError, match="ROICAI_API_KEY"):
        Roicai()


@respx.mock
def test_errors_carry_the_error_body(client: Roicai) -> None:
    respx.get(f"{BASE}/v3.0.0/tickers/NOPE:X").mock(return_value=error(404, "resource_missing"))
    with pytest.raises(NotFoundError) as raised:
        client.tickers.retrieve("NOPE:X")
    e = raised.value
    assert (e.status_code, e.code, e.type, e.request_id) == (
        404,
        "resource_missing",
        "invalid_request_error",
        "req_123",
    )
    assert str(e) == "HTTP 404: Something went wrong. (code: resource_missing, request_id: req_123)"


@respx.mock
def test_to_pandas_types_columns_from_the_schema(client: Roicai) -> None:
    respx.get(STATEMENTS).mock(
        side_effect=[
            httpx.Response(200, json=page([statement(2025), statement(2024, fiscal_year=None)], "tok2")),
            httpx.Response(200, json=page([statement(2023, is_net_income=None)])),
        ]
    )
    df = client.fundamentals.income_statements.list("NASDAQ:AAPL").to_pandas()
    assert len(df) == 3
    assert list(df.columns[:5]) == ["id", "symbol", "period_type", "period_end_date", "fiscal_year"]
    assert "object" not in df.columns
    assert str(df["fiscal_year"].dtype) == "Int64"
    assert df["fiscal_year"].isna().tolist() == [False, True, False]
    assert str(df["period_end_date"].dtype).startswith("datetime64")
    assert df["is_net_income"].dtype == "float64"
    assert str(df["fx_applied"].dtype) == "boolean"


@respx.mock
def test_to_polars_types_columns_from_the_schema(client: Roicai) -> None:
    import polars as pl

    respx.get(STATEMENTS).mock(return_value=httpx.Response(200, json=page([statement(2025), statement(2024)])))
    df = client.fundamentals.income_statements.list("NASDAQ:AAPL").to_polars()
    assert df.columns[:3] == ["id", "symbol", "period_type"]
    assert df.schema["period_end_date"] == pl.Date
    assert df.schema["fiscal_year"] == pl.Int64
    assert df.schema["is_net_income"] == pl.Float64
    assert df["period_end_date"][0] == dt.date(2025, 9, 30)


@respx.mock
def test_an_empty_list_still_has_its_columns(client: Roicai) -> None:
    respx.get(STATEMENTS).mock(return_value=httpx.Response(200, json=page([])))
    pager = client.fundamentals.income_statements.list("NASDAQ:AAPL")
    assert pager.to_pandas().columns[:2].tolist() == ["id", "symbol"]
    assert pager.to_polars().columns[:2] == ["id", "symbol"]


@respx.mock
def test_max_items_stops_and_warns(client: Roicai) -> None:
    route = respx.get(STATEMENTS).mock(
        side_effect=[
            httpx.Response(200, json=page([statement(2025), statement(2024)], "tok2")),
            httpx.Response(200, json=page([statement(2023), statement(2022)], "tok3")),
            httpx.Response(200, json=page([statement(2025)])),
        ]
    )
    with pytest.warns(UserWarning, match="max_items=3"):
        df = client.fundamentals.income_statements.list("NASDAQ:AAPL").to_pandas(max_items=3)
    assert len(df) == 3
    assert len(route.calls) == 2
    with pytest.raises(ValueError):
        client.fundamentals.income_statements.list("NASDAQ:AAPL").to_pandas(max_items=0)


@respx.mock
def test_max_items_equal_to_the_list_does_not_warn(client: Roicai) -> None:
    respx.get(STATEMENTS).mock(return_value=httpx.Response(200, json=page([statement(2025), statement(2024)])))
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert len(client.fundamentals.income_statements.list("NASDAQ:AAPL").to_pandas(max_items=2)) == 2


@respx.mock
def test_a_single_object_is_one_row(client: Roicai) -> None:
    respx.get(f"{BASE}/v3.0.0/tickers/NASDAQ:AAPL").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "tkr_1",
                "object": "v3.reference.ticker",
                "symbol": "AAPL",
                "name": "Apple Inc.",
                "exchange": "NASDAQ",
                "status": "listed",
            },
        )
    )
    df = client.tickers.retrieve("NASDAQ:AAPL").to_pandas()
    assert len(df) == 1
    assert df.loc[0, "name"] == "Apple Inc."


def test_a_missing_extra_says_how_to_install_it(client: Roicai, monkeypatch: pytest.MonkeyPatch) -> None:
    from roicai import TickerList

    monkeypatch.setitem(sys.modules, "polars", None)
    with pytest.raises(ImportError, match=r'pip install "roicai\[polars\]"'):
        TickerList(data=[], next_page_url=None, previous_page_url=None).to_polars()


@respx.mock
async def test_async_pages_and_frames(async_client: AsyncRoicai) -> None:
    route = respx.get(STATEMENTS).mock(
        side_effect=[
            httpx.Response(200, json=page([statement(2025)], "tok2")),
            httpx.Response(200, json=page([statement(2024)])),
        ]
    )
    pager = await async_client.fundamentals.income_statements.list("NASDAQ:AAPL", fiscal_year_lt=2026)
    df = await pager.to_pandas()
    assert df["fiscal_year"].tolist() == [2025, 2024]
    assert query(route.calls.last.request) == {"fiscal_year.lt": "2026", "page": "tok2"}
