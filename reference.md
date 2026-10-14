# Reference
## Exchanges
<details><summary><code>client.exchanges.<a href="src/roicai/exchanges/client.py">list</a>() -> ExchangeList</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns every exchange in one response, with segment MICs, names, markets, and symbol counts. Each code can be passed to the ticker-list exchange filter.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.exchanges.list()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Markets
<details><summary><code>client.markets.<a href="src/roicai/markets/client.py">list</a>() -> MarketList</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns every market in one response, with its exchanges, listing country, and symbol count. Each code can be passed to the ticker-search market filter.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.markets.list()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Sectors
<details><summary><code>client.sectors.<a href="src/roicai/sectors/client.py">list</a>() -> SectorList</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns every company sector in one response, with symbol counts.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.sectors.list()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Industries
<details><summary><code>client.industries.<a href="src/roicai/industries/client.py">list</a>() -> IndustryList</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns every company industry in one response, with symbol counts.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.industries.list()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Countries
<details><summary><code>client.countries.<a href="src/roicai/countries/client.py">list</a>() -> CountryList</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns every company country in one response, with names, ISO codes, and symbol counts.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.countries.list()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Tickers
<details><summary><code>client.tickers.<a href="src/roicai/tickers/client.py">list</a>(...) -> TickerList</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns a filtered page of ticker resources.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.tickers.list()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**exchange:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**type:** `typing.Optional[str]` — Filter by exact security type: 'dr', 'fund', or 'stock'.
    
</dd>
</dl>

<dl>
<dd>

**is_primary:** `typing.Optional[bool]` 
    
</dd>
</dl>

<dl>
<dd>

**status:** `typing.Optional[TickerStatus]` 
    
</dd>
</dl>

<dl>
<dd>

**listing_country_code:** `typing.Optional[str]` — Filter by two-letter listing country code: the country of the exchange where the ticker trades, not the company's domicile, e.g. 'US' or 'JP'.
    
</dd>
</dl>

<dl>
<dd>

**order:** `typing.Optional[Order]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Maximum number of resources to return. Defaults to 500.
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[str]` — Page token from a previous page's `next_page_url`. Iterating over the result fetches the next pages for you.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.tickers.<a href="src/roicai/tickers/client.py">search</a>(...) -> TickerList</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Ranks ticker codes and qualified symbols with typo-tolerant ranking by default. Set 'search_by' to 'name' to rank company names, or to another ticker field (such as 'isin' or 'figi') to match that field exactly.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.tickers.search(
    query="query",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**query:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**search_by:** `typing.Optional[SearchTickersRequestSearchBy]` — Fields used for matching. 'symbol' (the default) ranks ticker codes and qualified symbols; 'name' ranks company names. Any other value matches that exact ticker field.
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Maximum number of resources to return. Defaults to 500.
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[str]` — Page token from a previous page's `next_page_url`. Iterating over the result fetches the next pages for you.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.tickers.<a href="src/roicai/tickers/client.py">retrieve</a>(...) -> Ticker</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieves one ticker by public ID or supported market identifier.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.tickers.retrieve(
    identifier="NASDAQ:AAPL",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**identifier:** `str` — A ticker ID, an exchange and symbol separated by a colon (e.g. `NASDAQ:AAPL`), or a FIGI.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## StockSplits
<details><summary><code>client.stock_splits.<a href="src/roicai/stock_splits/client.py">list</a>(...) -> StockSplitList</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns a page of per-ticker stock-split events across all tickers, or one ticker via the identifier filter.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.stock_splits.list(
    identifier="NASDAQ:AAPL",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**identifier:** `typing.Optional[str]` — Restrict results to a single ticker. Accepts an exchange and symbol separated by a colon (e.g. `NASDAQ:AAPL`), a ticker ID, or a FIGI. Stock splits are per ticker, so results are the split events for that exact listing. Omit to list splits across all tickers.
    
</dd>
</dl>

<dl>
<dd>

**date:** `typing.Optional[str]` — Return splits executed on exactly this date.
    
</dd>
</dl>

<dl>
<dd>

**date_gte:** `typing.Optional[str]` — Return splits whose execution date is on or after this date.
    
</dd>
</dl>

<dl>
<dd>

**date_gt:** `typing.Optional[str]` — Return splits whose execution date is strictly after this date.
    
</dd>
</dl>

<dl>
<dd>

**date_lte:** `typing.Optional[str]` — Return splits whose execution date is on or before this date.
    
</dd>
</dl>

<dl>
<dd>

**date_lt:** `typing.Optional[str]` — Return splits whose execution date is strictly before this date.
    
</dd>
</dl>

<dl>
<dd>

**order:** `typing.Optional[Order]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Maximum number of resources to return. Defaults to 100.
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[str]` — Page token from a previous page's `next_page_url`. Iterating over the result fetches the next pages for you.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## StockPrices
<details><summary><code>client.stock_prices.<a href="src/roicai/stock_prices/client.py">list</a>(...) -> HistoricalPriceList</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns a page of historical daily prices for a ticker, symbol, or other supported security identifier.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.stock_prices.list(
    identifier="NASDAQ:AAPL",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**identifier:** `str` — A ticker ID, an exchange and symbol separated by a colon (e.g. `NASDAQ:AAPL`), or a FIGI.
    
</dd>
</dl>

<dl>
<dd>

**date:** `typing.Optional[str]` — Return prices from exactly this date.
    
</dd>
</dl>

<dl>
<dd>

**date_gte:** `typing.Optional[str]` — Return prices whose date is on or after this date.
    
</dd>
</dl>

<dl>
<dd>

**date_gt:** `typing.Optional[str]` — Return prices whose date is strictly after this date.
    
</dd>
</dl>

<dl>
<dd>

**date_lte:** `typing.Optional[str]` — Return prices whose date is on or before this date.
    
</dd>
</dl>

<dl>
<dd>

**date_lt:** `typing.Optional[str]` — Return prices whose date is strictly before this date.
    
</dd>
</dl>

<dl>
<dd>

**adjustment:** `typing.Optional[ListStockPricesRequestAdjustment]` 
    
</dd>
</dl>

<dl>
<dd>

**adjusted:** `typing.Optional[ListStockPricesRequestAdjusted]` 
    
</dd>
</dl>

<dl>
<dd>

**order:** `typing.Optional[Order]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Maximum number of resources to return. Defaults to 250.
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[str]` — Page token from a previous page's `next_page_url`. Iterating over the result fetches the next pages for you.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## ForexPairs
<details><summary><code>client.forex_pairs.<a href="src/roicai/forex_pairs/client.py">list</a>(...) -> ForexPairList</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns a page of tradable currency pairs with their currency codes and human-readable names. Use a pair `symbol` from this list with the forex price endpoints.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.forex_pairs.list(
    base_currency="EUR",
    quote_currency="EUR",
    currency="EUR",
    search="yen",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**base_currency:** `typing.Optional[str]` — Return only pairs quoted from this base currency.
    
</dd>
</dl>

<dl>
<dd>

**quote_currency:** `typing.Optional[str]` — Return only pairs quoted into this quote currency.
    
</dd>
</dl>

<dl>
<dd>

**currency:** `typing.Optional[str]` — Return every pair in which this currency appears, on either side.
    
</dd>
</dl>

<dl>
<dd>

**search:** `typing.Optional[str]` — Case-insensitive substring match against the pair symbol, both currency codes, and the human-readable name.
    
</dd>
</dl>

<dl>
<dd>

**order:** `typing.Optional[Order]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Maximum number of resources to return. Defaults to 500.
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[str]` — Page token from a previous page's `next_page_url`. Iterating over the result fetches the next pages for you.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## ForexPrices
<details><summary><code>client.forex_prices.<a href="src/roicai/forex_prices/client.py">list</a>(...) -> ForexPriceList</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns a page of historical daily prices for a currency pair, addressed by bare currency-pair code or qualified pair symbol.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.forex_prices.list(
    identifier="EURUSD",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**identifier:** `str` — A currency pair as `BASEQUOTE` or `BASE/QUOTE`, or a qualified pair symbol (e.g. `FX:EURUSD`). The `symbol` of every `/forex-pairs` result is accepted here.
    
</dd>
</dl>

<dl>
<dd>

**date:** `typing.Optional[str]` — Return prices from exactly this date.
    
</dd>
</dl>

<dl>
<dd>

**date_gte:** `typing.Optional[str]` — Return prices whose date is on or after this date.
    
</dd>
</dl>

<dl>
<dd>

**date_gt:** `typing.Optional[str]` — Return prices whose date is strictly after this date.
    
</dd>
</dl>

<dl>
<dd>

**date_lte:** `typing.Optional[str]` — Return prices whose date is on or before this date.
    
</dd>
</dl>

<dl>
<dd>

**date_lt:** `typing.Optional[str]` — Return prices whose date is strictly before this date.
    
</dd>
</dl>

<dl>
<dd>

**order:** `typing.Optional[Order]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Maximum number of resources to return. Defaults to 250.
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[str]` — Page token from a previous page's `next_page_url`. Iterating over the result fetches the next pages for you.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## EarningsCalls
<details><summary><code>client.earnings_calls.<a href="src/roicai/earnings_calls/client.py">list</a>(...) -> EarningsCallList</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns earnings-call summaries across all companies. Free plans can access each company’s latest two calls; paid-plan history follows the plan’s lookback limit. Filter by company identifier, fiscal period, or a call-date range, then retrieve a full transcript by company identifier and fiscal period.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.earnings_calls.list(
    identifier="NASDAQ:AAPL",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**identifier:** `typing.Optional[str]` — Restrict results to a single company. Accepts an exchange and symbol separated by a colon (e.g. `NASDAQ:AAPL`), a ticker ID, or a FIGI; the response `symbol` echoes the listing you requested. Omit to list earnings calls across all companies.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year:** `typing.Optional[int]` — Return only calls that report on this fiscal year, within the caller’s plan entitlement.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_quarter:** `typing.Optional[int]` — Return only calls that report on this fiscal quarter, from 1 to 4, within the caller’s plan entitlement.
    
</dd>
</dl>

<dl>
<dd>

**date:** `typing.Optional[str]` — Return calls that occurred on this UTC calendar date.
    
</dd>
</dl>

<dl>
<dd>

**date_gte:** `typing.Optional[str]` — Return calls on or after this UTC calendar date.
    
</dd>
</dl>

<dl>
<dd>

**date_gt:** `typing.Optional[str]` — Return calls after this UTC calendar date.
    
</dd>
</dl>

<dl>
<dd>

**date_lte:** `typing.Optional[str]` — Return calls on or before this UTC calendar date.
    
</dd>
</dl>

<dl>
<dd>

**date_lt:** `typing.Optional[str]` — Return calls before this UTC calendar date.
    
</dd>
</dl>

<dl>
<dd>

**order:** `typing.Optional[Order]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Maximum number of resources to return. Defaults to 50.
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[str]` — Page token from a previous page's `next_page_url`. Iterating over the result fetches the next pages for you.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.earnings_calls.<a href="src/roicai/earnings_calls/client.py">retrieve</a>(...) -> EarningsCall</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns one complete earnings-call transcript for a company and fiscal period. Free plans can retrieve the company’s latest two calls; paid-plan history follows the plan’s lookback limit. Identify the company by an exchange and symbol separated by a colon (e.g. `NASDAQ:AAPL`), a ticker ID, or a FIGI, and select the call with the `fiscal_year` and `fiscal_quarter` query parameters.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.earnings_calls.retrieve(
    identifier="NASDAQ:AAPL",
    fiscal_year=1,
    fiscal_quarter=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**identifier:** `str` — The company whose transcript to retrieve. Accepts an exchange and symbol separated by a colon (e.g. `NASDAQ:AAPL`), a ticker ID, or a FIGI.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year:** `int` — The fiscal year the call reports on, within the caller’s plan entitlement.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_quarter:** `int` — The fiscal quarter the call reports on, from 1 to 4, within the caller’s plan entitlement.
    
</dd>
</dl>

<dl>
<dd>

**format:** `typing.Optional[RetrieveEarningsCallsRequestFormat]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Company Events
<details><summary><code>client.company_events.<a href="src/roicai/company_events/client.py">list</a>(...) -> CompanyEventList</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns earnings events with everything attached to them: the transcript in `transcripts`, one entry per edition (`raw` and `edited`) with a stable id, audio recordings, slide decks, and filings. Only events with at least one of those are listed, newest fiscal period first. Free plans see each company’s latest two events; Individual plans follow the plan’s lookback; Professional and Enterprise plans see everything. Filter by company identifier or by content kind.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.company_events.list(
    identifier="NASDAQ:AAPL",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**identifier:** `typing.Optional[str]` — Restrict results to a single company. Accepts an exchange and symbol separated by a colon (e.g. `NASDAQ:AAPL`), a ticker ID, or a FIGI; the response `symbol` echoes the listing you requested. Omit to list events across all companies.
    
</dd>
</dl>

<dl>
<dd>

**content:** `typing.Optional[ListCompanyEventsRequestContent]` 
    
</dd>
</dl>

<dl>
<dd>

**order:** `typing.Optional[Order]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Maximum number of resources to return. Defaults to 50.
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[str]` — Page token from a previous page's `next_page_url`. Iterating over the result fetches the next pages for you.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Calendar Earnings
<details><summary><code>client.calendar.earnings.<a href="src/roicai/calendar/earnings/client.py">list</a>(...) -> EarningsEventList</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns a page of dated earnings events across all tickers, or one ticker via the identifier filter. Each event carries the scheduled release date and session plus EPS and revenue estimates, actuals, and surprises.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.calendar.earnings.list(
    identifier="NASDAQ:AAPL",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**identifier:** `typing.Optional[str]` — Restrict results to a single ticker. Accepts an exchange and symbol separated by a colon (e.g. `NASDAQ:AAPL`), a ticker ID, or a FIGI. Omit to list earnings events across all tickers.
    
</dd>
</dl>

<dl>
<dd>

**date:** `typing.Optional[str]` — Return events whose release date is exactly this date.
    
</dd>
</dl>

<dl>
<dd>

**date_gte:** `typing.Optional[str]` — Return events whose release date is on or after this date.
    
</dd>
</dl>

<dl>
<dd>

**date_gt:** `typing.Optional[str]` — Return events whose release date is strictly after this date.
    
</dd>
</dl>

<dl>
<dd>

**date_lte:** `typing.Optional[str]` — Return events whose release date is on or before this date.
    
</dd>
</dl>

<dl>
<dd>

**date_lt:** `typing.Optional[str]` — Return events whose release date is strictly before this date.
    
</dd>
</dl>

<dl>
<dd>

**order:** `typing.Optional[Order]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Maximum number of resources to return. Defaults to 100.
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[str]` — Page token from a previous page's `next_page_url`. Iterating over the result fetches the next pages for you.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Companies Profiles
<details><summary><code>client.companies.profiles.<a href="src/roicai/companies/profiles/client.py">retrieve</a>(...) -> CompanyProfile</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieves a primary-listing company profile by public profile ID or supported market identifier.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.companies.profiles.retrieve(
    identifier="NASDAQ:AAPL",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**identifier:** `str` — A company-profile ID, ticker ID, an exchange and symbol separated by a colon (e.g. `NASDAQ:AAPL`), or a FIGI.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Companies Employees
<details><summary><code>client.companies.employees.<a href="src/roicai/companies/employees/client.py">list</a>(...) -> EmployeeCountList</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns a page of fiscal-year employee counts across all companies, or one company via the identifier filter. Any listing identifier resolves to the primary company record.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.companies.employees.list(
    identifier="NASDAQ:AAPL",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**identifier:** `typing.Optional[str]` — Restrict results to a single company. Accepts a company-profile ID, a ticker ID, an exchange and symbol separated by a colon (e.g. `NASDAQ:AAPL`), or a FIGI. Employee counts are company-level data, so secondary listings resolve to the primary listing. Omit to list counts across all companies.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year:** `typing.Optional[int]` — Return only counts for exactly this fiscal year.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_gte:** `typing.Optional[int]` — Return counts from this fiscal year onward.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_gt:** `typing.Optional[int]` — Return counts after this fiscal year.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_lte:** `typing.Optional[int]` — Return counts through this fiscal year.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_lt:** `typing.Optional[int]` — Return counts before this fiscal year.
    
</dd>
</dl>

<dl>
<dd>

**order:** `typing.Optional[Order]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Maximum number of resources to return. Defaults to 100.
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[str]` — Page token from a previous page's `next_page_url`. Iterating over the result fetches the next pages for you.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Companies Logos
<details><summary><code>client.companies.logos.<a href="src/roicai/companies/logos/client.py">retrieve</a>(...) -> typing.Iterator[bytes]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns a resized company logo as WebP or PNG image bytes. Secondary listings resolve to the primary company logo.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.companies.logos.retrieve(
    identifier="identifier",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**identifier:** `str` — A company-profile ID, ticker ID, an exchange and symbol separated by a colon (e.g. `NASDAQ:AAPL`), or a FIGI.
    
</dd>
</dl>

<dl>
<dd>

**size:** `typing.Optional[int]` — Square image size in pixels. Defaults to 128.
    
</dd>
</dl>

<dl>
<dd>

**greyscale:** `typing.Optional[bool]` — Whether to remove color from the logo. Defaults to false.
    
</dd>
</dl>

<dl>
<dd>

**format:** `typing.Optional[RetrieveLogosRequestFormat]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Documents Slides
<details><summary><code>client.documents.slides.<a href="src/roicai/documents/slides/client.py">retrieve</a>(...) -> SlidesDownload</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns the metadata of an earnings-event slide deck together with a signed download URL that expires at `expires_at` (one hour by default). Professional and Enterprise plans only. Use the `doc_` id from the event’s `slides` list.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.documents.slides.retrieve(
    id="doc_4JlukNobJIA1qj",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The document id from the event listing (`doc_...`).
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Documents Filings
<details><summary><code>client.documents.filings.<a href="src/roicai/documents/filings/client.py">retrieve</a>(...) -> DocumentDownload</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns the metadata of an earnings-event filing (earnings release, quarterly or annual report, and similar) together with a signed download URL that expires at `expires_at` (one hour by default). Professional and Enterprise plans only. Use the `doc_` id from the event’s `filings` list.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.documents.filings.retrieve(
    id="doc_4JlukNobJIA1qj",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The document id from the event listing (`doc_...`).
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Documents Audio
<details><summary><code>client.documents.audio.<a href="src/roicai/documents/audio/client.py">retrieve</a>(...) -> AudioDownload</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns the metadata of an earnings-call audio recording together with a signed download URL that expires at `expires_at` (one hour by default). Professional and Enterprise plans only. Use the `audio_` id from the event’s `audio` list.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.documents.audio.retrieve(
    id="audio_7Ft0XPWQVpVeJ1",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The audio id from the event listing (`audio_...`).
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Documents Transcripts Raw
<details><summary><code>client.documents.transcripts.raw.<a href="src/roicai/documents/transcripts/raw/client.py">retrieve</a>(...) -> TranscriptRaw</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns the plain-text transcript of an earnings event, without speaker labels or line breaks, from a ready Quartr transcript when one exists, otherwise from the FMP transcript. Free plans can read each company’s latest two events; Individual plans follow the plan’s lookback; Professional and Enterprise plans read everything. Use the `trraw_` id from the event listing.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.documents.transcripts.raw.retrieve(
    id="trraw_hbBlbCUawzMoz0",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The transcript id from the event listing: `trraw_...` for the raw edition, `tredit_...` for the edited edition. Both are keyed by the event and stay stable when the source changes.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Documents Transcripts Edited
<details><summary><code>client.documents.transcripts.edited.<a href="src/roicai/documents/transcripts/edited/client.py">retrieve</a>(...) -> TranscriptEdited</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns the speaker-labelled transcript of an earnings event: ordered segments with a `speaker_id`, and a `speakers` map with each speaker’s name, role, and company where known. Quartr transcripts prefer the human-edited edition, then the aligned edition; FMP transcripts derive speakers from the turn names. Professional and Enterprise plans only. Use the `tredit_` id from the event listing.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.documents.transcripts.edited.retrieve(
    id="trraw_hbBlbCUawzMoz0",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The transcript id from the event listing: `trraw_...` for the raw edition, `tredit_...` for the edited edition. Both are keyed by the event and stay stable when the source changes.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## EarningsCalls Bulk
<details><summary><code>client.earnings_calls.bulk.<a href="src/roicai/earnings_calls/bulk/client.py">list</a>(...) -> BulkFileList</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists pre-generated transcript CSV files partitioned by fiscal year and quarter, each with a short-lived signed download URL. Filter with the optional year and period parameters. Requires a Professional or Enterprise plan.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.earnings_calls.bulk.list()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**year:** `typing.Optional[int]` — Return only the files of this year. Fiscal year for fundamentals and earnings calls, calendar year for stock prices.
    
</dd>
</dl>

<dl>
<dd>

**period:** `typing.Optional[ListBulkRequestPeriod]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Exchanges TradingHours
<details><summary><code>client.exchanges.trading_hours.<a href="src/roicai/exchanges/trading_hours/client.py">retrieve</a>(...) -> ExchangeTradingHours</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieves the complete regular and extended trading-hours history of one exchange as structured arrays.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.exchanges.trading_hours.retrieve(
    exchange="exchange",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**exchange:** `str` — Exchange code to retrieve trading-hours history for, e.g. NASDAQ.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Exchanges Holidays
<details><summary><code>client.exchanges.holidays.<a href="src/roicai/exchanges/holidays/client.py">retrieve</a>(...) -> ExchangeHolidays</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieves the holiday calendar of one exchange by exchange code, as YYYY-MM-DD dates.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.exchanges.holidays.retrieve(
    exchange="exchange",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**exchange:** `str` — Exchange code to retrieve the holiday calendar for, e.g. NASDAQ.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## ForexPrices Latest
<details><summary><code>client.forex_prices.latest.<a href="src/roicai/forex_prices/latest/client.py">list</a>(...) -> LatestForexPriceList</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns a page with one row per currency pair carrying its latest available daily OHLC quote from the last 10 days. Pairs without a price in that window appear with null price fields. Requires an Individual or higher plan.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.forex_prices.latest.list(
    base_currency="EUR",
    quote_currency="EUR",
    currency="EUR",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**base_currency:** `typing.Optional[str]` — Return only pairs quoted from this base currency.
    
</dd>
</dl>

<dl>
<dd>

**quote_currency:** `typing.Optional[str]` — Return only pairs quoted into this quote currency.
    
</dd>
</dl>

<dl>
<dd>

**currency:** `typing.Optional[str]` — Return every pair in which this currency appears, on either side.
    
</dd>
</dl>

<dl>
<dd>

**order:** `typing.Optional[Order]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Maximum number of resources to return. Defaults to 500.
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[str]` — Page token from a previous page's `next_page_url`. Iterating over the result fetches the next pages for you.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.forex_prices.latest.<a href="src/roicai/forex_prices/latest/client.py">retrieve</a>(...) -> ForexPrice</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns the latest available daily price for a currency pair, addressed by bare currency-pair code or qualified pair symbol.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.forex_prices.latest.retrieve(
    identifier="EURUSD",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**identifier:** `str` — A currency pair as `BASEQUOTE` or `BASE/QUOTE`, or a qualified pair symbol (e.g. `FX:EURUSD`). The `symbol` of every `/forex-pairs` result is accepted here.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Fundamentals IncomeStatements
<details><summary><code>client.fundamentals.income_statements.<a href="src/roicai/fundamentals/income_statements/client.py">list</a>(...) -> IncomeStatementFinancialPeriodList</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns income-statement line items by financial period.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.fundamentals.income_statements.list(
    identifier="NASDAQ:AAPL",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**identifier:** `str` — A ticker ID, an exchange and symbol separated by a colon (e.g. `NASDAQ:AAPL`), or a FIGI.
    
</dd>
</dl>

<dl>
<dd>

**period_type:** `typing.Optional[PeriodType]` 
    
</dd>
</dl>

<dl>
<dd>

**period_label:** `typing.Optional[PeriodLabel]` 
    
</dd>
</dl>

<dl>
<dd>

**date:** `typing.Optional[str]` — Return statements whose period end date is exactly this date.
    
</dd>
</dl>

<dl>
<dd>

**date_gte:** `typing.Optional[str]` — Return statements whose period end date is on or after this date.
    
</dd>
</dl>

<dl>
<dd>

**date_gt:** `typing.Optional[str]` — Return statements whose period end date is strictly after this date.
    
</dd>
</dl>

<dl>
<dd>

**date_lte:** `typing.Optional[str]` — Return statements whose period end date is on or before this date.
    
</dd>
</dl>

<dl>
<dd>

**date_lt:** `typing.Optional[str]` — Return statements whose period end date is strictly before this date.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_gte:** `typing.Optional[int]` — Return statements from this fiscal year onward.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_gt:** `typing.Optional[int]` — Return statements after this fiscal year.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_lte:** `typing.Optional[int]` — Return statements through this fiscal year.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_lt:** `typing.Optional[int]` — Return statements before this fiscal year.
    
</dd>
</dl>

<dl>
<dd>

**order:** `typing.Optional[Order]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Maximum number of resources to return. Defaults to 50.
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[str]` — Page token from a previous page's `next_page_url`. Iterating over the result fetches the next pages for you.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Fundamentals BalanceSheets
<details><summary><code>client.fundamentals.balance_sheets.<a href="src/roicai/fundamentals/balance_sheets/client.py">list</a>(...) -> BalanceSheetFinancialPeriodList</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns balance-sheet line items by financial period.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.fundamentals.balance_sheets.list(
    identifier="NASDAQ:AAPL",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**identifier:** `str` — A ticker ID, an exchange and symbol separated by a colon (e.g. `NASDAQ:AAPL`), or a FIGI.
    
</dd>
</dl>

<dl>
<dd>

**period_type:** `typing.Optional[PeriodType]` 
    
</dd>
</dl>

<dl>
<dd>

**period_label:** `typing.Optional[PeriodLabel]` 
    
</dd>
</dl>

<dl>
<dd>

**date:** `typing.Optional[str]` — Return statements whose period end date is exactly this date.
    
</dd>
</dl>

<dl>
<dd>

**date_gte:** `typing.Optional[str]` — Return statements whose period end date is on or after this date.
    
</dd>
</dl>

<dl>
<dd>

**date_gt:** `typing.Optional[str]` — Return statements whose period end date is strictly after this date.
    
</dd>
</dl>

<dl>
<dd>

**date_lte:** `typing.Optional[str]` — Return statements whose period end date is on or before this date.
    
</dd>
</dl>

<dl>
<dd>

**date_lt:** `typing.Optional[str]` — Return statements whose period end date is strictly before this date.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_gte:** `typing.Optional[int]` — Return statements from this fiscal year onward.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_gt:** `typing.Optional[int]` — Return statements after this fiscal year.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_lte:** `typing.Optional[int]` — Return statements through this fiscal year.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_lt:** `typing.Optional[int]` — Return statements before this fiscal year.
    
</dd>
</dl>

<dl>
<dd>

**order:** `typing.Optional[Order]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Maximum number of resources to return. Defaults to 50.
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[str]` — Page token from a previous page's `next_page_url`. Iterating over the result fetches the next pages for you.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Fundamentals CashFlowStatements
<details><summary><code>client.fundamentals.cash_flow_statements.<a href="src/roicai/fundamentals/cash_flow_statements/client.py">list</a>(...) -> CashFlowFinancialPeriodList</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns cash-flow line items by financial period.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.fundamentals.cash_flow_statements.list(
    identifier="NASDAQ:AAPL",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**identifier:** `str` — A ticker ID, an exchange and symbol separated by a colon (e.g. `NASDAQ:AAPL`), or a FIGI.
    
</dd>
</dl>

<dl>
<dd>

**period_type:** `typing.Optional[PeriodType]` 
    
</dd>
</dl>

<dl>
<dd>

**period_label:** `typing.Optional[PeriodLabel]` 
    
</dd>
</dl>

<dl>
<dd>

**date:** `typing.Optional[str]` — Return statements whose period end date is exactly this date.
    
</dd>
</dl>

<dl>
<dd>

**date_gte:** `typing.Optional[str]` — Return statements whose period end date is on or after this date.
    
</dd>
</dl>

<dl>
<dd>

**date_gt:** `typing.Optional[str]` — Return statements whose period end date is strictly after this date.
    
</dd>
</dl>

<dl>
<dd>

**date_lte:** `typing.Optional[str]` — Return statements whose period end date is on or before this date.
    
</dd>
</dl>

<dl>
<dd>

**date_lt:** `typing.Optional[str]` — Return statements whose period end date is strictly before this date.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_gte:** `typing.Optional[int]` — Return statements from this fiscal year onward.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_gt:** `typing.Optional[int]` — Return statements after this fiscal year.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_lte:** `typing.Optional[int]` — Return statements through this fiscal year.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_lt:** `typing.Optional[int]` — Return statements before this fiscal year.
    
</dd>
</dl>

<dl>
<dd>

**order:** `typing.Optional[Order]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Maximum number of resources to return. Defaults to 50.
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[str]` — Page token from a previous page's `next_page_url`. Iterating over the result fetches the next pages for you.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Fundamentals EnterpriseValues
<details><summary><code>client.fundamentals.enterprise_values.<a href="src/roicai/fundamentals/enterprise_values/client.py">list</a>(...) -> EnterpriseValueFinancialPeriodList</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns enterprise values by financial period.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.fundamentals.enterprise_values.list(
    identifier="NASDAQ:AAPL",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**identifier:** `str` — A ticker ID, an exchange and symbol separated by a colon (e.g. `NASDAQ:AAPL`), or a FIGI.
    
</dd>
</dl>

<dl>
<dd>

**period_type:** `typing.Optional[PeriodType]` 
    
</dd>
</dl>

<dl>
<dd>

**period_label:** `typing.Optional[PeriodLabel]` 
    
</dd>
</dl>

<dl>
<dd>

**date:** `typing.Optional[str]` — Return statements whose period end date is exactly this date.
    
</dd>
</dl>

<dl>
<dd>

**date_gte:** `typing.Optional[str]` — Return statements whose period end date is on or after this date.
    
</dd>
</dl>

<dl>
<dd>

**date_gt:** `typing.Optional[str]` — Return statements whose period end date is strictly after this date.
    
</dd>
</dl>

<dl>
<dd>

**date_lte:** `typing.Optional[str]` — Return statements whose period end date is on or before this date.
    
</dd>
</dl>

<dl>
<dd>

**date_lt:** `typing.Optional[str]` — Return statements whose period end date is strictly before this date.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_gte:** `typing.Optional[int]` — Return statements from this fiscal year onward.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_gt:** `typing.Optional[int]` — Return statements after this fiscal year.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_lte:** `typing.Optional[int]` — Return statements through this fiscal year.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_lt:** `typing.Optional[int]` — Return statements before this fiscal year.
    
</dd>
</dl>

<dl>
<dd>

**order:** `typing.Optional[Order]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Maximum number of resources to return. Defaults to 50.
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[str]` — Page token from a previous page's `next_page_url`. Iterating over the result fetches the next pages for you.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Fundamentals Multiples
<details><summary><code>client.fundamentals.multiples.<a href="src/roicai/fundamentals/multiples/client.py">list</a>(...) -> ValuationMultiplesFinancialPeriodList</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns valuation multiples by financial period.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.fundamentals.multiples.list(
    identifier="NASDAQ:AAPL",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**identifier:** `str` — A ticker ID, an exchange and symbol separated by a colon (e.g. `NASDAQ:AAPL`), or a FIGI.
    
</dd>
</dl>

<dl>
<dd>

**period_type:** `typing.Optional[PeriodType]` 
    
</dd>
</dl>

<dl>
<dd>

**period_label:** `typing.Optional[PeriodLabel]` 
    
</dd>
</dl>

<dl>
<dd>

**date:** `typing.Optional[str]` — Return statements whose period end date is exactly this date.
    
</dd>
</dl>

<dl>
<dd>

**date_gte:** `typing.Optional[str]` — Return statements whose period end date is on or after this date.
    
</dd>
</dl>

<dl>
<dd>

**date_gt:** `typing.Optional[str]` — Return statements whose period end date is strictly after this date.
    
</dd>
</dl>

<dl>
<dd>

**date_lte:** `typing.Optional[str]` — Return statements whose period end date is on or before this date.
    
</dd>
</dl>

<dl>
<dd>

**date_lt:** `typing.Optional[str]` — Return statements whose period end date is strictly before this date.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_gte:** `typing.Optional[int]` — Return statements from this fiscal year onward.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_gt:** `typing.Optional[int]` — Return statements after this fiscal year.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_lte:** `typing.Optional[int]` — Return statements through this fiscal year.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_lt:** `typing.Optional[int]` — Return statements before this fiscal year.
    
</dd>
</dl>

<dl>
<dd>

**order:** `typing.Optional[Order]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Maximum number of resources to return. Defaults to 50.
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[str]` — Page token from a previous page's `next_page_url`. Iterating over the result fetches the next pages for you.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Fundamentals PerShareMetrics
<details><summary><code>client.fundamentals.per_share_metrics.<a href="src/roicai/fundamentals/per_share_metrics/client.py">list</a>(...) -> PerShareFinancialPeriodList</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns per-share metrics by financial period.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.fundamentals.per_share_metrics.list(
    identifier="NASDAQ:AAPL",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**identifier:** `str` — A ticker ID, an exchange and symbol separated by a colon (e.g. `NASDAQ:AAPL`), or a FIGI.
    
</dd>
</dl>

<dl>
<dd>

**period_type:** `typing.Optional[PeriodType]` 
    
</dd>
</dl>

<dl>
<dd>

**period_label:** `typing.Optional[PeriodLabel]` 
    
</dd>
</dl>

<dl>
<dd>

**date:** `typing.Optional[str]` — Return statements whose period end date is exactly this date.
    
</dd>
</dl>

<dl>
<dd>

**date_gte:** `typing.Optional[str]` — Return statements whose period end date is on or after this date.
    
</dd>
</dl>

<dl>
<dd>

**date_gt:** `typing.Optional[str]` — Return statements whose period end date is strictly after this date.
    
</dd>
</dl>

<dl>
<dd>

**date_lte:** `typing.Optional[str]` — Return statements whose period end date is on or before this date.
    
</dd>
</dl>

<dl>
<dd>

**date_lt:** `typing.Optional[str]` — Return statements whose period end date is strictly before this date.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_gte:** `typing.Optional[int]` — Return statements from this fiscal year onward.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_gt:** `typing.Optional[int]` — Return statements after this fiscal year.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_lte:** `typing.Optional[int]` — Return statements through this fiscal year.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_lt:** `typing.Optional[int]` — Return statements before this fiscal year.
    
</dd>
</dl>

<dl>
<dd>

**order:** `typing.Optional[Order]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Maximum number of resources to return. Defaults to 50.
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[str]` — Page token from a previous page's `next_page_url`. Iterating over the result fetches the next pages for you.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Fundamentals Bulk
<details><summary><code>client.fundamentals.bulk.<a href="src/roicai/fundamentals/bulk/client.py">list</a>(...) -> BulkFileList</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists pre-generated CSV files partitioned by fiscal year and financial cadence, each with a short-lived signed download URL. Filter with the optional year and period parameters. Requires a Professional or Enterprise plan.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.fundamentals.bulk.list()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**year:** `typing.Optional[int]` — Return only the files of this year. Fiscal year for fundamentals and earnings calls, calendar year for stock prices.
    
</dd>
</dl>

<dl>
<dd>

**period:** `typing.Optional[ListBulkRequestPeriod]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Fundamentals Ratios Profitability
<details><summary><code>client.fundamentals.ratios.profitability.<a href="src/roicai/fundamentals/ratios/profitability/client.py">list</a>(...) -> ProfitabilityFinancialPeriodList</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns profitability ratios by financial period.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.fundamentals.ratios.profitability.list(
    identifier="NASDAQ:AAPL",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**identifier:** `str` — A ticker ID, an exchange and symbol separated by a colon (e.g. `NASDAQ:AAPL`), or a FIGI.
    
</dd>
</dl>

<dl>
<dd>

**period_type:** `typing.Optional[PeriodType]` 
    
</dd>
</dl>

<dl>
<dd>

**period_label:** `typing.Optional[PeriodLabel]` 
    
</dd>
</dl>

<dl>
<dd>

**date_gte:** `typing.Optional[str]` — Return statements whose period end date is on or after this date.
    
</dd>
</dl>

<dl>
<dd>

**date_gt:** `typing.Optional[str]` — Return statements whose period end date is strictly after this date.
    
</dd>
</dl>

<dl>
<dd>

**date_lte:** `typing.Optional[str]` — Return statements whose period end date is on or before this date.
    
</dd>
</dl>

<dl>
<dd>

**date_lt:** `typing.Optional[str]` — Return statements whose period end date is strictly before this date.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_gte:** `typing.Optional[int]` — Return statements from this fiscal year onward.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_gt:** `typing.Optional[int]` — Return statements after this fiscal year.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_lte:** `typing.Optional[int]` — Return statements through this fiscal year.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_lt:** `typing.Optional[int]` — Return statements before this fiscal year.
    
</dd>
</dl>

<dl>
<dd>

**order:** `typing.Optional[Order]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Maximum number of resources to return. Defaults to 50.
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[str]` — Page token from a previous page's `next_page_url`. Iterating over the result fetches the next pages for you.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Fundamentals Ratios Credit
<details><summary><code>client.fundamentals.ratios.credit.<a href="src/roicai/fundamentals/ratios/credit/client.py">list</a>(...) -> CreditFinancialPeriodList</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns credit and debt values by financial period.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.fundamentals.ratios.credit.list(
    identifier="NASDAQ:AAPL",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**identifier:** `str` — A ticker ID, an exchange and symbol separated by a colon (e.g. `NASDAQ:AAPL`), or a FIGI.
    
</dd>
</dl>

<dl>
<dd>

**period_type:** `typing.Optional[PeriodType]` 
    
</dd>
</dl>

<dl>
<dd>

**period_label:** `typing.Optional[PeriodLabel]` 
    
</dd>
</dl>

<dl>
<dd>

**date_gte:** `typing.Optional[str]` — Return statements whose period end date is on or after this date.
    
</dd>
</dl>

<dl>
<dd>

**date_gt:** `typing.Optional[str]` — Return statements whose period end date is strictly after this date.
    
</dd>
</dl>

<dl>
<dd>

**date_lte:** `typing.Optional[str]` — Return statements whose period end date is on or before this date.
    
</dd>
</dl>

<dl>
<dd>

**date_lt:** `typing.Optional[str]` — Return statements whose period end date is strictly before this date.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_gte:** `typing.Optional[int]` — Return statements from this fiscal year onward.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_gt:** `typing.Optional[int]` — Return statements after this fiscal year.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_lte:** `typing.Optional[int]` — Return statements through this fiscal year.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_lt:** `typing.Optional[int]` — Return statements before this fiscal year.
    
</dd>
</dl>

<dl>
<dd>

**order:** `typing.Optional[Order]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Maximum number of resources to return. Defaults to 50.
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[str]` — Page token from a previous page's `next_page_url`. Iterating over the result fetches the next pages for you.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Fundamentals Ratios Liquidity
<details><summary><code>client.fundamentals.ratios.liquidity.<a href="src/roicai/fundamentals/ratios/liquidity/client.py">list</a>(...) -> LiquidityFinancialPeriodList</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns liquidity ratios by financial period.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.fundamentals.ratios.liquidity.list(
    identifier="NASDAQ:AAPL",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**identifier:** `str` — A ticker ID, an exchange and symbol separated by a colon (e.g. `NASDAQ:AAPL`), or a FIGI.
    
</dd>
</dl>

<dl>
<dd>

**period_type:** `typing.Optional[PeriodType]` 
    
</dd>
</dl>

<dl>
<dd>

**period_label:** `typing.Optional[PeriodLabel]` 
    
</dd>
</dl>

<dl>
<dd>

**date:** `typing.Optional[str]` — Return statements whose period end date is exactly this date.
    
</dd>
</dl>

<dl>
<dd>

**date_gte:** `typing.Optional[str]` — Return statements whose period end date is on or after this date.
    
</dd>
</dl>

<dl>
<dd>

**date_gt:** `typing.Optional[str]` — Return statements whose period end date is strictly after this date.
    
</dd>
</dl>

<dl>
<dd>

**date_lte:** `typing.Optional[str]` — Return statements whose period end date is on or before this date.
    
</dd>
</dl>

<dl>
<dd>

**date_lt:** `typing.Optional[str]` — Return statements whose period end date is strictly before this date.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_gte:** `typing.Optional[int]` — Return statements from this fiscal year onward.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_gt:** `typing.Optional[int]` — Return statements after this fiscal year.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_lte:** `typing.Optional[int]` — Return statements through this fiscal year.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_lt:** `typing.Optional[int]` — Return statements before this fiscal year.
    
</dd>
</dl>

<dl>
<dd>

**order:** `typing.Optional[Order]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Maximum number of resources to return. Defaults to 50.
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[str]` — Page token from a previous page's `next_page_url`. Iterating over the result fetches the next pages for you.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Fundamentals Ratios WorkingCapital
<details><summary><code>client.fundamentals.ratios.working_capital.<a href="src/roicai/fundamentals/ratios/working_capital/client.py">list</a>(...) -> WorkingCapitalFinancialPeriodList</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns working-capital ratios by financial period.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.fundamentals.ratios.working_capital.list(
    identifier="NASDAQ:AAPL",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**identifier:** `str` — A ticker ID, an exchange and symbol separated by a colon (e.g. `NASDAQ:AAPL`), or a FIGI.
    
</dd>
</dl>

<dl>
<dd>

**period_type:** `typing.Optional[PeriodType]` 
    
</dd>
</dl>

<dl>
<dd>

**period_label:** `typing.Optional[PeriodLabel]` 
    
</dd>
</dl>

<dl>
<dd>

**date:** `typing.Optional[str]` — Return statements whose period end date is exactly this date.
    
</dd>
</dl>

<dl>
<dd>

**date_gte:** `typing.Optional[str]` — Return statements whose period end date is on or after this date.
    
</dd>
</dl>

<dl>
<dd>

**date_gt:** `typing.Optional[str]` — Return statements whose period end date is strictly after this date.
    
</dd>
</dl>

<dl>
<dd>

**date_lte:** `typing.Optional[str]` — Return statements whose period end date is on or before this date.
    
</dd>
</dl>

<dl>
<dd>

**date_lt:** `typing.Optional[str]` — Return statements whose period end date is strictly before this date.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_gte:** `typing.Optional[int]` — Return statements from this fiscal year onward.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_gt:** `typing.Optional[int]` — Return statements after this fiscal year.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_lte:** `typing.Optional[int]` — Return statements through this fiscal year.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_lt:** `typing.Optional[int]` — Return statements before this fiscal year.
    
</dd>
</dl>

<dl>
<dd>

**order:** `typing.Optional[Order]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Maximum number of resources to return. Defaults to 50.
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[str]` — Page token from a previous page's `next_page_url`. Iterating over the result fetches the next pages for you.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Fundamentals Ratios YieldAnalysis
<details><summary><code>client.fundamentals.ratios.yield_analysis.<a href="src/roicai/fundamentals/ratios/yield_analysis/client.py">list</a>(...) -> YieldAnalysisFinancialPeriodList</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns yield-analysis ratios by financial period.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.fundamentals.ratios.yield_analysis.list(
    identifier="NASDAQ:AAPL",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**identifier:** `str` — A ticker ID, an exchange and symbol separated by a colon (e.g. `NASDAQ:AAPL`), or a FIGI.
    
</dd>
</dl>

<dl>
<dd>

**period_type:** `typing.Optional[PeriodType]` 
    
</dd>
</dl>

<dl>
<dd>

**period_label:** `typing.Optional[PeriodLabel]` 
    
</dd>
</dl>

<dl>
<dd>

**date:** `typing.Optional[str]` — Return statements whose period end date is exactly this date.
    
</dd>
</dl>

<dl>
<dd>

**date_gte:** `typing.Optional[str]` — Return statements whose period end date is on or after this date.
    
</dd>
</dl>

<dl>
<dd>

**date_gt:** `typing.Optional[str]` — Return statements whose period end date is strictly after this date.
    
</dd>
</dl>

<dl>
<dd>

**date_lte:** `typing.Optional[str]` — Return statements whose period end date is on or before this date.
    
</dd>
</dl>

<dl>
<dd>

**date_lt:** `typing.Optional[str]` — Return statements whose period end date is strictly before this date.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_gte:** `typing.Optional[int]` — Return statements from this fiscal year onward.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_gt:** `typing.Optional[int]` — Return statements after this fiscal year.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_lte:** `typing.Optional[int]` — Return statements through this fiscal year.
    
</dd>
</dl>

<dl>
<dd>

**fiscal_year_lt:** `typing.Optional[int]` — Return statements before this fiscal year.
    
</dd>
</dl>

<dl>
<dd>

**order:** `typing.Optional[Order]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Maximum number of resources to return. Defaults to 50.
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[str]` — Page token from a previous page's `next_page_url`. Iterating over the result fetches the next pages for you.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## StockPrices Latest
<details><summary><code>client.stock_prices.latest.<a href="src/roicai/stock_prices/latest/client.py">list</a>(...) -> LatestStockPriceList</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns a page with one row per ticker carrying its latest available daily OHLCV quote from the last 10 days. Tickers without a price in that window (halted, delisted, or unpriced listings) appear with null price fields. Requires an Individual or higher plan.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.stock_prices.latest.list()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**exchange:** `typing.Optional[str]` — Filter to tickers listed on one exchange code, e.g. `NASDAQ`.
    
</dd>
</dl>

<dl>
<dd>

**order:** `typing.Optional[Order]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Maximum number of resources to return. Defaults to 500.
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[str]` — Page token from a previous page's `next_page_url`. Iterating over the result fetches the next pages for you.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.stock_prices.latest.<a href="src/roicai/stock_prices/latest/client.py">retrieve</a>(...) -> HistoricalPrice</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns the latest available daily price for a ticker, symbol, or other supported security identifier.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.stock_prices.latest.retrieve(
    identifier="NASDAQ:AAPL",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**identifier:** `str` — A ticker ID, an exchange and symbol separated by a colon (e.g. `NASDAQ:AAPL`), or a FIGI.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## StockPrices Bulk
<details><summary><code>client.stock_prices.bulk.<a href="src/roicai/stock_prices/bulk/client.py">list</a>(...) -> BulkFileList</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists pre-generated daily-price CSV files partitioned by calendar year and month, each with a short-lived signed download URL. Filter with the optional year and period parameters. Requires a Professional or Enterprise plan.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from roicai import Roicai
from roicai.environment import RoicaiEnvironment

client = Roicai(
    api_key="<token>",
    environment=RoicaiEnvironment.DEFAULT,
)

client.stock_prices.bulk.list()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**year:** `typing.Optional[int]` — Return only the files of this year. Fiscal year for fundamentals and earnings calls, calendar year for stock prices.
    
</dd>
</dl>

<dl>
<dd>

**period:** `typing.Optional[ListBulkRequestPeriod]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

