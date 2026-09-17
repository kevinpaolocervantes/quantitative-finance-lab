import pandas as pd
import yfinance as yf


def load_portfolio(path):
    portfolio = pd.read_csv(path)
    if not {"ticker", "weight"}.issubset(portfolio.columns):
        raise ValueError("Portfolio CSV must contain ticker and weight columns.")

    portfolio = portfolio.copy()
    portfolio["ticker"] = portfolio["ticker"].astype(str).str.strip().str.upper()
    portfolio["weight"] = pd.to_numeric(portfolio["weight"], errors="raise")

    if portfolio["ticker"].duplicated().any():
        raise ValueError("Portfolio contains duplicate tickers.")
    if (portfolio["weight"] < 0).any():
        raise ValueError("Portfolio weights cannot be negative.")

    total = portfolio["weight"].sum()
    if total <= 0:
        raise ValueError("Portfolio weights must sum to a positive number.")

    portfolio["weight"] = portfolio["weight"] / total
    return portfolio


def download_adjusted_prices(tickers, period="3y"):
    data = yf.download(tickers, period=period, auto_adjust=True, progress=False)
    if data.empty:
        raise ValueError("No market data returned.")

    if isinstance(data.columns, pd.MultiIndex):
        prices = data["Close"]
    else:
        prices = data[["Close"]].rename(columns={"Close": tickers[0]})

    missing = [t for t in tickers if t not in prices.columns]
    if missing:
        raise ValueError(f"Missing price data for: {', '.join(missing)}")

    return prices[tickers].dropna(how="all")


def calculate_returns(prices):
    return prices.pct_change(fill_method=None).dropna(how="all")
