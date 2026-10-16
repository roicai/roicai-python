# ROIC.AI Python Library

[![PyPI](https://img.shields.io/pypi/v/roicai.svg)](https://pypi.org/project/roicai/)
[![Python versions](https://img.shields.io/pypi/pyversions/roicai.svg)](https://pypi.org/project/roicai/)
[![Build Status](https://github.com/roicai/roicai-python/actions/workflows/ci.yml/badge.svg)](https://github.com/roicai/roicai-python/actions/workflows/ci.yml)

The ROIC.AI Python library is the official Python client for the [ROIC.AI](https://www.roic.ai) financial data API and stock API. Use it to get fundamentals for public companies, such as income statements, balance sheets, cash flow statements, financial ratios and valuation multiples, and earnings call transcripts. It also covers historical and latest stock prices, SEC filings and other company documents, the earnings calendar, company profiles and forex rates.

Responses are typed Pydantic models, list methods fetch the next pages for you, and any response converts to a pandas or polars DataFrame.

## Documentation

See the [ROIC.AI API reference](https://api.roic.ai/v3.0.0/openapi) for every endpoint, parameter and field, and the [API guides](https://www.roic.ai/api) for authentication, plans and response formats. [reference.md](https://github.com/roicai/roicai-python/blob/main/reference.md) lists every method of this library with its parameters.

## Requirements

Python 3.10 or later.

## Installation

Install the package with:

```sh
pip install --upgrade roicai
```

To convert responses to DataFrames, install pandas or polars with it:

```sh
pip install --upgrade "roicai[pandas]"
pip install --upgrade "roicai[polars]"
```

These are the same package; the part in brackets also installs pandas or polars. With conda, install `pandas` or `polars` next to it.

## Usage

The library needs your ROIC.AI API key, which you can find on the [authentication page](https://www.roic.ai/api/docs/authentication) once you sign in. Set it as the `ROICAI_API_KEY` environment variable, or pass it to the client:

```python
from roicai import Roicai

client = Roicai()  # reads ROICAI_API_KEY
# or: client = Roicai(api_key="...")

ticker = client.tickers.retrieve("NASDAQ:AAPL")
print(ticker.name, ticker.exchange)

statements = client.fundamentals.income_statements.list(
    "NASDAQ:AAPL",
    period_type="annual",
    limit=5,
)
for year in statements.items:
    print(year.fiscal_year, year.is_sales_revenue_turnover, year.is_net_income)

latest = client.stock_prices.latest.retrieve("NASDAQ:AAPL")
print(latest.date, latest.close)
```

Methods are grouped the way the API's URLs are: `/v3.0.0/fundamental/ratios/credit/{identifier}` is `client.fundamentals.ratios.credit.list(...)`. Each group has `list`, `retrieve` or `search`.

Identify a company by its exchange and symbol separated by a colon (`NASDAQ:AAPL`), its ticker ID (`tkr_...`) or its FIGI.

### Types

Responses are [Pydantic](https://docs.pydantic.dev) models with the API's field names, which are snake_case. Dates are `datetime.date` and timestamps are timezone-aware `datetime.datetime`. Every parameter and field is typed, so your editor completes them and mypy or pyright checks your calls. Enums are string literals that also accept other strings, so values the API adds later still parse:

```python
from roicai import IncomeStatementFinancialPeriod

for statement in client.fundamentals.income_statements.list("NASDAQ:AAPL", period_type="annual", limit=3):
    row: IncomeStatementFinancialPeriod = statement
    print(row.period_end_date.year, row.period_type)  # e.g. 2025 annual

print(statement.model_dump()["fiscal_year"])
```

Use `model_dump()` for a dict and `model_dump_json()` for JSON.

### DataFrames

Call `to_pandas()` or `to_polars()` on any response. A list becomes one row per item:

```python
df = client.fundamentals.income_statements.list(
    "NASDAQ:AAPL",
    period_type="annual",
    fiscal_year_gte=2015,
).to_pandas()

print(df[["fiscal_year", "period_end_date", "is_sales_revenue_turnover", "is_net_income"]])
```

Columns are the API's fields, in the API's order, with `id`, `symbol` and the period first. Their types come from the API's schema: dates and timestamps are `datetime64` columns, whole numbers are nullable `Int64`, and amounts are `float64`. With polars, dates are `Date` columns.

On a list, `to_pandas()` and `to_polars()` convert the page you have: up to `limit` rows. If the list has more pages, they warn with a `MorePagesWarning`. Fetching the rest is up to you, since each page is one more request:

```python
prices = client.stock_prices.list("NASDAQ:AAPL", date_gte="2020-01-01", limit=1000)
closes = prices.to_polars(all_pages=True).select("date", "close")
print(closes.tail())

splits = client.stock_splits.list(identifier="NASDAQ:AAPL", limit=2).to_pandas(max_items=100)
first_five = client.tickers.list(exchange="NASDAQ", limit=5).to_pandas(all_pages=False)
```

| Argument | Rows |
|---|---|
| none | This page, with a warning if more pages remain. |
| `all_pages=True` | Every page. |
| `max_items=N` | This page and the next ones, up to N rows, with a warning if the list goes on. |
| `all_pages=False` | This page, without the warning. |

A single object, such as a ticker or a company profile, becomes a DataFrame with one row.

### Date and fiscal year ranges

Lists of dated rows take `date_gte`, `date_gt`, `date_lte` and `date_lt`, with dates as `"YYYY-MM-DD"` strings:

```python
january = client.stock_prices.list(
    "NASDAQ:AAPL",
    date_gte="2025-01-01",
    date_lte="2025-01-31",
    order="asc",
)
```

They work on stock prices, stock splits, forex prices, earnings calls, the earnings calendar and every fundamentals list. Fundamentals and employee counts also take `fiscal_year_gte`, `fiscal_year_gt`, `fiscal_year_lte` and `fiscal_year_lt`:

```python
since_2020 = client.fundamentals.income_statements.list(
    "NASDAQ:AAPL",
    period_type="annual",
    fiscal_year_gte=2020,
)
```

The library sends these under the API's names, such as `date.gte`.

### Auto-pagination

List methods return a page of up to `limit` items in `items`. Iterate over the page itself to get every item of every page: the library fetches each next page when it gets there, by sending the same request again with the page token from `next_page_url`, so every page uses your filters.

```python
for call in client.earnings_calls.list(identifier="NASDAQ:AAPL", limit=100):
    print(call.fiscal_year, call.fiscal_quarter, call.date)
```

Use `break` to stop early; the library requests no page after the one you stopped in.

To go page by page, use `iter_pages()`, or `next_page()`, which returns `None` after the last page:

```python
pager = client.tickers.list(exchange="NASDAQ", limit=500)
for page in pager.iter_pages():
    print(len(page.items), page.response.next_page_url)
    break
```

`response` holds the whole response model of each page.

### Async

`AsyncRoicai` has the same methods, as coroutines. Iterate over its lists with `async for`:

```python
import asyncio

from roicai import AsyncRoicai


async def main() -> None:
    async with AsyncRoicai() as client:
        ticker = await client.tickers.retrieve("NASDAQ:MSFT")
        print(ticker.name)

        pager = await client.fundamentals.ratios.profitability.list("NASDAQ:MSFT", period_type="annual")
        async for year in pager:
            print(year.fiscal_year, year.gross_margin)

        df = await pager.to_pandas()
        print(df.shape)


asyncio.run(main())
```

For many concurrent requests, install `roicai[aiohttp]`: `AsyncRoicai` then sends requests with aiohttp rather than httpx's own transport, unless you pass `httpx_client`.

## Handling errors

When the API returns an error, the library raises a subclass of `ApiError` for its status. Each has the HTTP `status_code` and the API's error fields: `message`, `type`, `code`, `param` and `request_id`, which you can quote to support:

```python
from roicai import ApiError, NotFoundError

try:
    client.tickers.retrieve("NASDAQ:NOPE")
except NotFoundError as e:
    print(e.code, e.message)  # resource_missing No ticker matches the supplied identifier.
except ApiError as e:
    print(e.status_code, e.request_id)
```

| Status | Error |
|---|---|
| 400 | `BadRequestError` |
| 401 | `UnauthorizedError`: the API key is missing or invalid |
| 402 | `PaymentRequiredError`: your plan doesn't include the data |
| 404 | `NotFoundError`: no such company or resource |
| 429 | `TooManyRequestsError`: you exceeded your rate limit |
| 500 | `InternalServerError` |
| 503 | `ServiceUnavailableError` |

A request that can't reach the API raises httpx's exception, such as `httpx.ConnectError` or `httpx.TimeoutException`.

## Configuration

Pass options to the client:

```python
import httpx

from roicai import Roicai

client = Roicai(
    api_key="...",
    timeout=20.0,
    max_retries=3,
    app_info={"name": "my-app", "version": "1.0"},
)
```

| Option | Default | Description |
|---|---|---|
| `api_key` | `ROICAI_API_KEY` | Your API key, sent as `Authorization: Bearer <key>`. |
| `base_url` | `https://api.roic.ai` | URL that requests are made to. |
| `timeout` | `60` | Seconds to wait for a response. With your own `httpx_client`, that client's timeout applies instead. |
| `max_retries` | `2` | Retries for a request that fails with a `408`, `409`, `429` or `5xx` status. |
| `headers` | | Headers sent with every request. |
| `app_info` | | Your application's `name`, and optionally `version` and `comment`, added to the `User-Agent`. If you build a library or plugin on ROIC.AI, please set it. |
| `httpx_client` | | [The httpx client that sends requests.](#configuring-the-http-client) |

### Retries

The library retries a request up to `max_retries` times when it fails with a `408`, `409`, `429` or `5xx` status, or can't connect. It waits as long as the response's `Retry-After` header asks, or with exponential backoff and jitter. Set `max_retries=0` to turn retries off.

### Per-request options

Every method takes `request_options`, which overrides the client's settings for that request:

```python
ticker = client.tickers.retrieve(
    "NASDAQ:AAPL",
    request_options={"timeout": 5, "max_retries": 0, "additional_headers": {"X-Trace": "abc"}},
)
```

It takes `timeout`, `max_retries`, `additional_headers` and `additional_query_parameters`.

### Response headers

`with_raw_response` returns the HTTP response alongside the model, such as to read the request ID. It works on methods that return one object, such as `retrieve`:

```python
raw = client.tickers.with_raw_response.retrieve("NASDAQ:AAPL")
print(raw.headers.get("request-id"), raw.data.name)
```

### Configuring the HTTP client

Pass your own `httpx.Client`, or `httpx.AsyncClient` for `AsyncRoicai`, to use a proxy, custom transports or event hooks:

```python
client = Roicai(
    httpx_client=httpx.Client(
        proxy="http://proxy.example.com:8080",
        timeout=30.0,
        event_hooks={"request": [lambda request: print(request.method, request.url)]},
    ),
)
```

### Closing the client

A client keeps its connections open for reuse. Close it when you're done, or use it as a context manager:

```python
with Roicai() as client:
    print(client.tickers.retrieve("NASDAQ:AAPL").name)
```

`AsyncRoicai` has `aclose()` and works with `async with`. A client you pass `httpx_client` to closes that client too.

### Logging

The library logs to the `roicai` logger. Pass `logging` to turn on its messages about requests and responses, which never include your API key:

```python
client = Roicai(logging={"level": "debug", "silent": False})
```

## Examples

The examples use the `client` from [Usage](#usage).

### Tickers

Retrieve one ticker, search by symbol or company name, or list tickers with filters:

```python
apple = client.tickers.retrieve("NASDAQ:AAPL")
print(apple.name, apple.isin, apple.figi)

by_symbol = client.tickers.search(query="AAPL", limit=5)
by_name = client.tickers.search(query="apple", search_by="name", limit=5)
by_isin = client.tickers.search(query="US0378331005", search_by="isin")
print([t.symbol for t in by_name.items])

nasdaq = client.tickers.list(exchange="NASDAQ", type="stock", status="listed", limit=100)
japan = client.tickers.list(listing_country_code="JP", is_primary=True)
```

`search_by` also matches `cik`, `cusip`, `figi` and the other ticker fields exactly.

### Company profile

```python
profile = client.companies.profiles.retrieve("NASDAQ:AAPL")
print(profile.name, profile.sector, profile.industry, profile.ceo)
print(profile.earnings_schedule.next_release_date)
```

### Stock prices

Historical daily prices come newest first. Prices are unadjusted unless you set `adjustment` to `"splits"` or `"total_return"`:

```python
prices = client.stock_prices.list("NASDAQ:AAPL", limit=30)
for day in prices.items:
    print(day.date, day.open, day.high, day.low, day.close, day.volume)
print(prices.response.currency)  # "USD"

split_adjusted = client.stock_prices.list("NASDAQ:AAPL", date="2020-08-28", adjustment="splits")

latest = client.stock_prices.latest.retrieve("NASDAQ:AAPL")
print(latest.date, latest.close)
```

For a date range, see [Date and fiscal year ranges](#date-and-fiscal-year-ranges).

### Financial statements

Income statements, balance sheets and cash flow statements take the same parameters. Set `period_type` to `"annual"`, `"quarterly"` or `"ttm"`, and `period_label` to one fiscal period (`"FY"`, `"Q1"` to `"Q4"`):

```python
annual = client.fundamentals.income_statements.list("NASDAQ:AAPL", period_type="annual", limit=5)
for year in annual.items:
    print(year.fiscal_year, year.is_sales_revenue_turnover, year.is_net_income, year.diluted_eps)

quarters = client.fundamentals.balance_sheets.list("NASDAQ:AAPL", period_type="quarterly", limit=4)
print([(q.fiscal_year, q.period_label, q.bs_tot_asset, q.bs_tot_liab) for q in quarters.items])

fourth_quarters = client.fundamentals.cash_flow_statements.list(
    "NASDAQ:AAPL",
    period_type="quarterly",
    period_label="Q4",
    limit=4,
)
print([(q.fiscal_year, q.cf_cash_from_oper, q.cf_free_cash_flow) for q in fourth_quarters.items])
```

Rows come newest first. Amounts are in `currency`, and line items use short names: `is_sales_revenue_turnover` is revenue, `bs_tot_asset` is total assets and `cf_cap_expenditures` is capital expenditures. `client.fundamentals.per_share_metrics` and `client.fundamentals.enterprise_values` work the same way.

### Ratios and multiples

Ratios are grouped into `profitability`, `credit`, `liquidity`, `working_capital` and `yield_analysis`. Margins and returns are percentages (`46.9` is 46.9%):

```python
profitability = client.fundamentals.ratios.profitability.list("NASDAQ:AAPL", period_type="annual", limit=5)
for year in profitability.items:
    print(year.fiscal_year, year.gross_margin, year.oper_margin, year.return_on_inv_capital)

credit = client.fundamentals.ratios.credit.list("NASDAQ:AAPL", limit=1)
print(credit.items[0].net_debt_to_ebitda)

multiples = client.fundamentals.multiples.list("NASDAQ:AAPL", period_type="quarterly", limit=1)
last = multiples.items[0]
print(last.pe_ratio, last.ev_to_ttm_ebitda, last.pr_to_book_ratio, last.pr_to_free_cash_flow)
```

### Earnings call transcripts

List a company's earnings calls, then retrieve a transcript by fiscal year and quarter. Free plans can access each company's latest two calls:

```python
calls = client.earnings_calls.list(identifier="NASDAQ:AAPL", limit=8)
print([(c.fiscal_year, c.fiscal_quarter, c.date) for c in calls.items])

call = client.earnings_calls.retrieve("NASDAQ:AAPL", fiscal_year=2026, fiscal_quarter=3)
if isinstance(call.transcript, list):
    for turn in call.transcript[:3]:
        print(f"{turn.speaker}: {turn.text[:80]}")

text = client.earnings_calls.retrieve("NASDAQ:AAPL", fiscal_year=2026, fiscal_quarter=3, format="text")
print(type(text.transcript))  # <class 'str'>
```

By default `transcript` is a list of turns with `speaker` and `text`. With `format="text"` it is one string.

Leave out `identifier` to list calls from every company, and filter by `date`, `fiscal_year` or `fiscal_quarter`:

```python
same_day = client.earnings_calls.list(date="2026-07-30")
```

### Earnings calendar

Each event has the release date and session, and the EPS and revenue estimates and actuals:

```python
schedule = client.calendar.earnings.list(identifier="NASDAQ:AAPL", limit=4)
for event in schedule.items:
    print(event.fiscal_period, event.release_date, event.release_session, event.eps_estimate, event.eps_actual)

one_day = client.calendar.earnings.list(date="2026-10-28")
```

### SEC filings and company documents

A company event is one reporting period, with the IDs of its transcripts, call audio, slides and filings, such as 10-Q and 8-K reports. Retrieve a document by ID to get a signed download URL, which needs no API key:

```python
events = client.company_events.list(identifier="NASDAQ:AAPL", limit=4)
event = events.items[0]
print(event.fiscal_year, event.fiscal_quarter, event.release_date)

filing = next((f for f in event.filings if f.form == "10-Q"), None)
if filing:
    download = client.documents.filings.retrieve(filing.id)
    print(download.filename, download.url, download.expires_at)

with_slides = client.company_events.list(identifier="NASDAQ:AAPL", content="slides")
```

`client.documents.slides`, `audio`, `transcripts.edited` and `transcripts.raw` retrieve the other kinds by ID.

### Company logos

`retrieve` returns the image as chunks of bytes:

```python
with open("aapl.webp", "wb") as f:
    for chunk in client.companies.logos.retrieve("NASDAQ:AAPL"):
        f.write(chunk)
```

### Forex

Identify a currency pair as `FX:` followed by the base and quote currencies:

```python
pairs = client.forex_pairs.list(base_currency="EUR", quote_currency="USD")
yen = client.forex_pairs.list(search="yen")

eurusd = client.forex_prices.list("FX:EURUSD", limit=30)
print([(day.date, day.close) for day in eurusd.items])

rate = client.forex_prices.latest.retrieve("FX:EURUSD")
print(rate.date, rate.close)

to_usd = client.forex_prices.latest.list(quote_currency="USD")
```

## Support

Report bugs and request features in [GitHub issues](https://github.com/roicai/roicai-python/issues). For questions about your account, plan or the data, contact ROIC.AI through [www.roic.ai](https://www.roic.ai).

The library follows semver. While it is `0.x`, a minor version can include breaking changes, so pin the minor version you use.

## Contributing

See [CONTRIBUTING.md](https://github.com/roicai/roicai-python/blob/main/CONTRIBUTING.md) to build and test the library, regenerate it from the API, and release it.

## License

[MIT](https://github.com/roicai/roicai-python/blob/main/LICENSE)
