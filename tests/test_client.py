"""Offline tests of the hand-written behaviour, with the HTTP layer mocked."""

from __future__ import annotations

import datetime as dt
import sys
import warnings
from urllib.parse import parse_qs, urlsplit

import httpx
import pytest
import respx

from roicai import (
    ApiError,
    AsyncRoicai,
    MorePagesWarning,
    NotFoundError,
    Roicai,
    TooManyRequestsError,
    __version__,
)
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
    df = client.fundamentals.income_statements.list("NASDAQ:AAPL").to_pandas(all_pages=True)
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
    with pytest.warns(MorePagesWarning, match="max_items=3"):
        df = client.fundamentals.income_statements.list("NASDAQ:AAPL").to_pandas(max_items=3)
    assert len(df) == 3
    assert len(route.calls) == 2
    with pytest.raises(ValueError):
        client.fundamentals.income_statements.list("NASDAQ:AAPL").to_pandas(max_items=0)


@respx.mock
def test_max_items_at_the_end_of_a_page_does_not_fetch_the_next(client: Roicai) -> None:
    route = respx.get(STATEMENTS).mock(
        side_effect=[
            httpx.Response(200, json=page([statement(2025), statement(2024)], "tok2")),
            httpx.Response(200, json=page([statement(2023)])),
        ]
    )
    with pytest.warns(MorePagesWarning, match="max_items=2"):
        df = client.fundamentals.income_statements.list("NASDAQ:AAPL").to_pandas(max_items=2)
    assert len(df) == 2
    assert len(route.calls) == 1


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
    df = await pager.to_pandas(all_pages=True)
    assert df["fiscal_year"].tolist() == [2025, 2024]
    assert query(route.calls.last.request) == {"fiscal_year.lt": "2026", "page": "tok2"}


@respx.mock
def test_next_page_is_none_on_the_last_page(client: Roicai) -> None:
    route = respx.get(STATEMENTS).mock(
        side_effect=[
            httpx.Response(200, json=page([statement(2025)], "tok2")),
            httpx.Response(200, json=page([statement(2024)])),
        ]
    )
    first = client.fundamentals.income_statements.list("NASDAQ:AAPL")
    second = first.next_page()
    assert second is not None and [r.fiscal_year for r in second.items or []] == [2024]
    assert second.next_page() is None
    assert len(route.calls) == 2


@respx.mock
async def test_async_next_page_is_none_on_the_last_page(async_client: AsyncRoicai) -> None:
    route = respx.get(STATEMENTS).mock(return_value=httpx.Response(200, json=page([statement(2025)])))
    pager = await async_client.fundamentals.income_statements.list("NASDAQ:AAPL")
    assert await pager.next_page() is None
    assert len(route.calls) == 1


@pytest.fixture
def sleeps(monkeypatch: pytest.MonkeyPatch) -> list:
    """Records the waits between retries instead of waiting."""
    import roicai.core.http_client as http_client

    waits: list = []

    async def asleep(seconds: float) -> None:
        waits.append(seconds)

    monkeypatch.setattr(http_client.time, "sleep", waits.append)
    monkeypatch.setattr(http_client.asyncio, "sleep", asleep)
    return waits


@respx.mock
def test_streamed_responses_are_retried(sleeps: list) -> None:
    route = respx.get(f"{BASE}/v3.0.0/company/logo/NASDAQ:AAPL").mock(
        side_effect=[
            httpx.Response(429, headers={"Retry-After": "3"}, json={"error": {"message": "slow down"}}),
            httpx.Response(503, headers={"Retry-After": "1"}),
            httpx.Response(200, content=b"RIFFlogo"),
        ]
    )
    client = Roicai(api_key="test_key", max_retries=2)
    assert b"".join(client.companies.logos.retrieve("NASDAQ:AAPL")) == b"RIFFlogo"
    assert len(route.calls) == 3
    assert sleeps == [3, 1]


@respx.mock
def test_streamed_responses_stop_after_max_retries(sleeps: list) -> None:
    route = respx.get(f"{BASE}/v3.0.0/company/logo/NASDAQ:AAPL").mock(
        return_value=httpx.Response(429, headers={"Retry-After": "0"}, json=error(429, "rate_limited").json())
    )
    client = Roicai(api_key="test_key", max_retries=1)
    with pytest.raises(TooManyRequestsError):
        b"".join(client.companies.logos.retrieve("NASDAQ:AAPL"))
    assert len(route.calls) == 2


@respx.mock
async def test_async_streamed_responses_are_retried(sleeps: list) -> None:
    route = respx.get(f"{BASE}/v3.0.0/company/logo/NASDAQ:AAPL").mock(
        side_effect=[httpx.Response(500, headers={"Retry-After": "2"}), httpx.Response(200, content=b"RIFF")]
    )
    client = AsyncRoicai(api_key="test_key", max_retries=2, httpx_client=httpx.AsyncClient())
    chunks = [chunk async for chunk in client.companies.logos.retrieve("NASDAQ:AAPL")]
    assert b"".join(chunks) == b"RIFF"
    assert len(route.calls) == 2
    assert sleeps == [2]


def test_model_dump_honours_include_and_exclude() -> None:
    from roicai import CompanyProfileEarningsSchedule, IncomeStatementFinancialPeriod

    row = IncomeStatementFinancialPeriod.model_validate(statement(2025))
    assert row.model_dump(include={"id", "fiscal_year"}) == {"id": "fnd_2025", "fiscal_year": 2025}
    assert "fiscal_year" not in row.model_dump(exclude={"fiscal_year"})
    assert "fiscal_year" not in row.model_dump_json(exclude={"fiscal_year"})
    assert row.model_dump_json(include={"id", "symbol"}) == '{"id":"fnd_2025","symbol":"NASDAQ:AAPL"}'
    assert '"period_end_date":"2025-09-30"' in row.model_dump_json()
    profile_time = CompanyProfileEarningsSchedule.model_validate({"last_release_time": "2026-07-30T20:33:00Z"})
    assert '"last_release_time":"2026-07-30T20:33:00Z"' in profile_time.model_dump_json()


@respx.mock
async def test_async_token_needs_no_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ROICAI_API_KEY", raising=False)
    route = respx.get(STATEMENTS).mock(return_value=httpx.Response(200, json=page([])))

    async def token() -> str:
        return "fresh_token"

    client = AsyncRoicai(async_token=token, httpx_client=httpx.AsyncClient())
    await client.fundamentals.income_statements.list("NASDAQ:AAPL")
    assert route.calls.last.request.headers["authorization"] == "Bearer fresh_token"
    with pytest.raises(ApiError, match="ROICAI_API_KEY"):
        AsyncRoicai()


def test_an_empty_api_key_is_a_missing_one(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ROICAI_API_KEY", "")
    with pytest.raises(ApiError, match="No API key"):
        Roicai()
    with pytest.raises(ApiError, match="No API key"):
        AsyncRoicai(api_key="")


def test_every_group_resolves() -> None:
    def walk(group: object, depth: int = 0) -> int:
        found = 0
        for name, value in vars(type(group)).items():
            if isinstance(value, property) and not name.startswith("_") and name != "with_raw_response":
                found += 1 + walk(getattr(group, name), depth + 1)
        return found

    assert walk(Roicai(api_key="k")) >= 30
    assert walk(AsyncRoicai(api_key="k")) >= 30


def test_clients_close() -> None:
    with Roicai(api_key="k") as client:
        pass
    assert client._client_wrapper.httpx_client.httpx_client.is_closed


async def test_async_clients_close() -> None:
    async with AsyncRoicai(api_key="k", httpx_client=httpx.AsyncClient()) as client:
        pass
    assert client._client_wrapper.httpx_client.httpx_client.is_closed


@respx.mock
def test_path_parameters_are_percent_encoded(client: Roicai) -> None:
    route = respx.get(url__regex=rf"{BASE}/v3\.0\.0/tickers/.*").mock(return_value=error(404, "resource_missing"))
    with pytest.raises(NotFoundError):
        client.tickers.retrieve("NYSE:BRK/B?x=1#f")
    assert route.calls.last.request.url.raw_path == b"/v3.0.0/tickers/NYSE%3ABRK%2FB%3Fx%3D1%23f"


@respx.mock
def test_an_error_body_that_is_not_the_api_error_keeps_its_class(client: Roicai) -> None:
    from roicai import ServiceUnavailableError

    respx.get(f"{BASE}/v3.0.0/tickers/A").mock(
        side_effect=[
            httpx.Response(503, text="<html>Bad gateway</html>"),
            httpx.Response(429, json={"message": "Too Many Requests"}),
            httpx.Response(404),
        ]
    )
    with pytest.raises(ServiceUnavailableError) as unavailable:
        client.tickers.retrieve("A")
    assert unavailable.value.body == "<html>Bad gateway</html>"
    with pytest.raises(TooManyRequestsError) as limited:
        client.tickers.retrieve("A")
    assert limited.value.body == {"message": "Too Many Requests"}
    with pytest.raises(NotFoundError):
        client.tickers.retrieve("A")


@respx.mock
def test_errors_pickle_and_copy(client: Roicai) -> None:
    import copy
    import pickle

    respx.get(f"{BASE}/v3.0.0/tickers/A").mock(return_value=error(404, "resource_missing"))
    with pytest.raises(NotFoundError) as raised:
        client.tickers.retrieve("A")
    for clone in (pickle.loads(pickle.dumps(raised.value)), copy.copy(raised.value), copy.deepcopy(raised.value)):
        assert type(clone) is NotFoundError
        assert (clone.status_code, clone.code, clone.request_id) == (404, "resource_missing", "req_123")
    assert repr(raised.value) == (
        "NotFoundError(status_code=404, message='Something went wrong.', code='resource_missing', request_id='req_123')"
    )


@respx.mock
def test_max_items_must_be_a_positive_int(client: Roicai) -> None:
    respx.get(STATEMENTS).mock(return_value=httpx.Response(200, json=page([])))
    pager = client.fundamentals.income_statements.list("NASDAQ:AAPL")
    for bad in (True, 0, -1, 2.5):
        with pytest.raises(ValueError):
            pager.to_pandas(max_items=bad)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="all_pages=False"):
        pager.to_pandas(max_items=5, all_pages=False)
    with pytest.raises(ValueError):
        pager.to_pandas(all_pages="yes")  # type: ignore[arg-type]


def test_importing_adds_no_log_handler() -> None:
    import subprocess

    code = "import logging, roicai; roicai.Roicai(api_key='k'); print(len(logging.getLogger('roicai').handlers))"
    assert subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True).stdout == "0\n"


def two_pages() -> list:
    return [
        httpx.Response(200, json=page([statement(2025), statement(2024)], "tok2")),
        httpx.Response(200, json=page([statement(2023)])),
    ]


@respx.mock
def test_by_default_a_list_converts_this_page_and_warns(client: Roicai) -> None:
    route = respx.get(STATEMENTS).mock(side_effect=two_pages())
    pager = client.fundamentals.income_statements.list("NASDAQ:AAPL", limit=2)
    with pytest.warns(MorePagesWarning, match=r"to_pandas\(\) converted this page of 2 rows"):
        df = pager.to_pandas()
    assert df["fiscal_year"].tolist() == [2025, 2024]
    with pytest.warns(MorePagesWarning, match=r"to_polars\(\)"):
        assert pager.to_polars().height == 2
    assert len(route.calls) == 1


@respx.mock
def test_all_pages_false_converts_this_page_without_a_warning(client: Roicai) -> None:
    route = respx.get(STATEMENTS).mock(side_effect=two_pages())
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        df = client.fundamentals.income_statements.list("NASDAQ:AAPL", limit=2).to_pandas(all_pages=False)
    assert len(df) == 2
    assert len(route.calls) == 1


@respx.mock
def test_the_last_page_converts_without_a_warning(client: Roicai) -> None:
    respx.get(STATEMENTS).mock(return_value=httpx.Response(200, json=page([statement(2025)])))
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert len(client.fundamentals.income_statements.list("NASDAQ:AAPL").to_pandas()) == 1


@respx.mock
def test_all_pages_fetches_every_page(client: Roicai) -> None:
    route = respx.get(STATEMENTS).mock(side_effect=two_pages())
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        df = client.fundamentals.income_statements.list("NASDAQ:AAPL", limit=2).to_polars(all_pages=True)
    assert df["fiscal_year"].to_list() == [2025, 2024, 2023]
    assert len(route.calls) == 2


@respx.mock
async def test_async_default_converts_this_page(async_client: AsyncRoicai) -> None:
    route = respx.get(STATEMENTS).mock(side_effect=two_pages())
    pager = await async_client.fundamentals.income_statements.list("NASDAQ:AAPL", limit=2)
    with pytest.warns(MorePagesWarning):
        df = await pager.to_pandas()
    assert len(df) == 2
    assert len(route.calls) == 1
