"""Run the equity portfolio factor model."""

import argparse

from src.equity_factor_model.data import (
    FACTOR_PROXIES,
    calculate_returns,
    download_adjusted_prices,
    load_portfolio,
)
from src.equity_factor_model.model import (
    build_factor_returns,
    build_portfolio_returns,
    fit_factor_model,
)
from src.equity_factor_model.report import print_report, save_report


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Estimate historical factor exposures for an equity portfolio."
    )
    parser.add_argument(
        "--portfolio",
        default="examples/sample_portfolio.csv",
        help="Path to a CSV containing ticker and weight columns.",
    )
    parser.add_argument(
        "--period",
        default="3y",
        help="Yahoo Finance history period, such as 1y, 3y, or 5y.",
    )
    parser.add_argument(
        "--output",
        default="outputs/factor_exposures.csv",
        help="Path for the output CSV report.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    portfolio = load_portfolio(args.portfolio)

    portfolio_tickers = portfolio["ticker"].tolist()
    proxy_tickers = list(FACTOR_PROXIES.values())
    all_tickers = portfolio_tickers + proxy_tickers

    prices = download_adjusted_prices(all_tickers, period=args.period)
    returns = calculate_returns(prices)

    portfolio_returns = build_portfolio_returns(
        returns,
        portfolio,
    )
    factor_returns = build_factor_returns(
        returns,
        FACTOR_PROXIES,
    )

    result = fit_factor_model(
        portfolio_returns,
        factor_returns,
    )

    print_report(portfolio, result)
    save_report(result, args.output)

    print(f"\nCSV report saved to: {args.output}")


if __name__ == "__main__":
    main()
