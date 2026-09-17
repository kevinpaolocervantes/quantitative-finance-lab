"""Run the Portfolio Risk Engine."""

import argparse

from src.portfolio_risk_engine.data import calculate_returns, download_adjusted_prices, load_portfolio
from src.portfolio_risk_engine.report import print_report, save_report
from src.portfolio_risk_engine.risk import build_portfolio_returns, calculate_risk_contributions, calculate_risk_metrics


def parse_arguments():
    parser = argparse.ArgumentParser(description="Analyze portfolio risk.")
    parser.add_argument("--portfolio", default="examples/sample_portfolio.csv")
    parser.add_argument("--period", default="3y")
    parser.add_argument("--risk-free-rate", type=float, default=0.0)
    parser.add_argument("--confidence", type=float, default=0.95)
    parser.add_argument("--output", default=None)
    return parser.parse_args()


def main():
    args = parse_arguments()
    if not 0 < args.confidence < 1:
        raise ValueError("Confidence must be between 0 and 1.")

    portfolio = load_portfolio(args.portfolio)
    tickers = portfolio["ticker"].tolist()
    weights = portfolio.set_index("ticker")["weight"]

    prices = download_adjusted_prices(tickers, period=args.period)
    asset_returns = calculate_returns(prices)
    portfolio_returns = build_portfolio_returns(asset_returns, weights)

    metrics = calculate_risk_metrics(
        portfolio_returns,
        risk_free_rate=args.risk_free_rate,
        confidence=args.confidence,
    )
    contributions = calculate_risk_contributions(asset_returns, weights)

    print_report(metrics, contributions, args.confidence)

    if args.output:
        save_report(metrics, contributions, args.output)


if __name__ == "__main__":
    main()
