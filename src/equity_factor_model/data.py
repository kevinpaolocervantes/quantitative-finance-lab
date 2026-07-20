"""Market data and portfolio input utilities."""

from pathlib import Path
from typing import Sequence

import pandas as pd
import yfinance as yf


FACTOR_PROXIES = {
    "market": "SPY",
    "size": "IWM",
    "value": "IWD",
    "momentum": "MTUM",
    "quality": "QUAL",
    "low_volatility": "USMV",
}


def load_portfolio(path: str | Path) -> pd.DataFrame:
    """Load and validate a portfolio CSV containing ticker and weight columns."""

    portfolio = pd.read_csv(path)

    required_columns = {"ticker", "weight"}
    missing_columns = required_columns.difference(portfolio.columns)

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Portfolio is missing required columns: {missing}")

    portfolio = portfolio.copy()
    portfolio["ticker"] = portfolio["ticker"].astype(str).str.upper().str.strip()
    portfolio["weight"] = pd.to_numeric(portfolio["weight"], errors="raise")

    if portfolio["ticker"].duplicated().any():
        duplicates = portfolio.loc[
            portfolio["ticker"].duplicated(), "ticker"
        ].tolist()
        raise ValueError(f"Duplicate portfolio tickers: {duplicates}")

    if (portfolio["weight"] < 0).any():
        raise ValueError("Portfolio weights cannot be negative.")

    total_weight = float(portfolio["weight"].sum())

    if total_weight <= 0:
        raise ValueError("Portfolio weights must sum to a positive number.")

    portfolio["weight"] = portfolio["weight"] / total_weight

    return portfolio


def download_adjusted_prices(
    tickers: Sequence[str],
    period: str = "3y",
) -> pd.DataFrame:
    """Download adjusted closing prices from Yahoo Finance."""

    unique_tickers = list(dict.fromkeys(tickers))

    if not unique_tickers:
        raise ValueError("At least one ticker is required.")

    downloaded = yf.download(
        tickers=unique_tickers,
        period=period,
        auto_adjust=True,
        progress=False,
        group_by="column",
    )

    if downloaded.empty:
        raise RuntimeError("No market data was downloaded.")

    if isinstance(downloaded.columns, pd.MultiIndex):
        prices = downloaded["Close"].copy()
    else:
        prices = downloaded[["Close"]].copy()
        prices.columns = unique_tickers

    if isinstance(prices, pd.Series):
        prices = prices.to_frame()

    prices = prices.dropna(axis=1, how="all").sort_index()

    missing_tickers = sorted(set(unique_tickers).difference(prices.columns))

    if missing_tickers:
        missing = ", ".join(missing_tickers)
        raise RuntimeError(f"No usable price data found for: {missing}")

    return prices


def calculate_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Convert adjusted prices into daily percentage returns."""

    returns = prices.pct_change(fill_method=None)
    return returns.dropna(how="all")
