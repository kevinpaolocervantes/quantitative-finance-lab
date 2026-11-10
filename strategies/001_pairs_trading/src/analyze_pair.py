"""Stage 1: Download and examine KO/PEP adjusted prices and daily returns.

Research only. No trading signals or investment recommendations.
"""
from pathlib import Path
import argparse
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]


def get_prices(start: str, end: str, symbols=('KO', 'PEP')) -> pd.DataFrame:
    # auto_adjust=True adjusts for dividends and splits; use these for return analysis.
    raw = yf.download(list(symbols), start=start, end=end, auto_adjust=True,
                      progress=False, threads=False)
    if raw.empty:
        raise RuntimeError('No data returned. Check network access and dates.')
    prices = raw['Close'] if isinstance(raw.columns, pd.MultiIndex) else raw[['Close']]
    if not isinstance(prices.columns, pd.MultiIndex):
        if len(symbols) == 1:
            prices.columns = [symbols[0]]
    prices = prices.reindex(columns=list(symbols)).dropna(how='any')
    if len(prices) < 60:
        raise ValueError('Need at least 60 overlapping daily price observations.')
    return prices


def analyze(prices: pd.DataFrame):
    returns = prices.pct_change().dropna()
    correlation = float(returns.iloc[:, 0].corr(returns.iloc[:, 1]))
    indexed = prices.div(prices.iloc[0]).mul(100)
    return returns, indexed, correlation


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start', default='2021-11-01')
    parser.add_argument('--end', default='2026-11-09', help='Exclusive end date')
    args = parser.parse_args()
    out = ROOT / 'outputs'
    out.mkdir(exist_ok=True)
    prices = get_prices(args.start, args.end)
    returns, indexed, corr = analyze(prices)
    prices.to_csv(out / 'adjusted_prices.csv')
    returns.to_csv(out / 'daily_returns.csv')
    fig, ax = plt.subplots(figsize=(10, 5))
    indexed.plot(ax=ax)
    ax.set(title=f'KO vs PEP: adjusted total-return price index (start = 100)\nDaily return correlation: {corr:.3f}', ylabel='Index (start = 100)', xlabel='Date')
    fig.tight_layout()
    fig.savefig(out / 'normalized_prices.png', dpi=160)
    plt.close(fig)
    print(f'Observations: {len(prices)} | {prices.index.min().date()} to {prices.index.max().date()}')
    print(f'Daily return correlation: {corr:.4f}')
    print(f'Saved outputs to: {out}')
    print('Correlation does NOT establish cointegration or profitability.')


if __name__ == '__main__':
    main()
