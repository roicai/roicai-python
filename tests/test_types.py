"""Checked by mypy and pyright, not run: the types users see from the SDK."""

from __future__ import annotations

import datetime as dt
import typing

import pandas
import polars

from roicai import AsyncRoicai, IncomeStatementFinancialPeriod, Roicai, Ticker


def sync_usage(client: Roicai) -> None:
    pager = client.fundamentals.income_statements.list("NASDAQ:AAPL", period_type="annual", fiscal_year_gte=2015)
    for row in pager:
        statement: IncomeStatementFinancialPeriod = row
        ended: dt.date = row.period_end_date
        year: typing.Optional[int] = row.fiscal_year
    frame: pandas.DataFrame = pager.to_pandas(all_pages=True)
    pl_frame: polars.DataFrame = pager.to_polars(max_items=500)
    ticker: Ticker = client.tickers.retrieve("NASDAQ:AAPL")
    one_row: pandas.DataFrame = ticker.to_pandas()
    every_exchange: polars.DataFrame = client.exchanges.list().to_polars()

    # The checkers must catch these: an unused ignore is an error in both.
    client.tickers.retrieve(123)  # type: ignore[arg-type]
    client.fundamentals.income_statements.list("NASDAQ:AAPL", limit="5")  # type: ignore[arg-type]
    name: int = ticker.symbol  # type: ignore[assignment]


async def async_usage(client: AsyncRoicai) -> None:
    pager = await client.fundamentals.income_statements.list("NASDAQ:AAPL")
    async for row in pager:
        statement: IncomeStatementFinancialPeriod = row
    frame: pandas.DataFrame = await pager.to_pandas()
