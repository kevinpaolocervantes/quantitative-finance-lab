"""Command-line entry point for the equity portfolio factor model."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from src.equity_factor_model.data import (
    FACTOR_PROXIES,
    calculate_returns,
    download_adjusted_prices,
    load_portfolio,
)
from src.equity_factor_model.model import (
    FactorModelResult,
    build_factor_returns,
    build_portfolio_returns,
    fit_factor_model,
)
from src.equity_factor_model.report import print_report, save_report


LOGGER = logging.getLogger(__name__)

VALID_PERIODS = {
    "1mo",
    "3mo",
    "6mo",
    "1y",
    "2y",
    "3y",
    "5y",
    "10y",
    "ytd",
    "max",
}


def valid_portfolio_path(value: str) -> Path:
    """Validate that the portfolio file exists and is a CSV."""

    path = Path(value).expanduser()

    if not path.exists():
        raise argparse.ArgumentTypeError(
            f"Portfolio file does not exist: {path}"
        )

    if not path.is_file():
        raise argparse.ArgumentTypeError(
            f"Portfolio path is not a file: {path}"
        )

    if path.suffix.lower() != ".csv":
        raise argparse.ArgumentTypeError(
            "Portfolio input must be a CSV file."
        )

    return path


def valid_period(value: str) -> str:
    """Validate a supported Yahoo Finance period."""

    normalized = value.lower().strip()

    if normalized not in VALID_PERIODS:
        supported = ", ".join(sorted(VALID_PERIODS))
        raise argparse.ArgumentTypeError(
            f"Unsupported period '{value}'. Choose from: {supported}"
        )

    return normalized


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description=(
            "Estimate historical factor exposures for a weighted "
            "equity portfolio."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--portfolio",
        type=valid_portfolio_path,
        default=Path("examples/sample_portfolio.csv"),
        help="CSV file containing ticker and weight columns.",
    )

    parser.add_argument(
        "--period",
        type=valid_period,
        default="3y",
        help="Historical market-data period.",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/factor_exposures.csv"),
        help="Destination for the CSV factor report.",
    )

    parser.add_argument(
        "--log-level",
        choices=("DEBUG", "INFO", "WARNING", "ERROR"),
        default="INFO",
        help="Logging verbosity.",
    )

    return parser.parse_args()


def configure_logging(level: str) -> None:
    """Configure application logging."""

    logging.basicConfig(
        level=getattr(logging, level),
        format="%(levelname)s: %(message)s",
    )


def collect_required_tickers(
    portfolio_tickers: list[str],
) -> list[str]:
    """Combine portfolio and factor-proxy tickers without duplicates."""

    proxy_tickers = list(FACTOR_PROXIES.values())

    return list(
        dict.fromkeys(portfolio_tickers + proxy_tickers)
    )


def run_factor_analysis(
    portfolio_path: Path,
    period: str,
) -> tuple:
    """
    Run the complete factor-analysis workflow.

    Returns the validated portfolio and fitted model result.
    """

    LOGGER.info("Loading portfolio from %s", portfolio_path)
    portfolio = load_portfolio(portfolio_path)

    portfolio_tickers = portfolio["ticker"].tolist()
    required_tickers = collect_required_tickers(portfolio_tickers)

    LOGGER.info(
        "Downloading %s of market data for %d tickers",
        period,
        len(required_tickers),
    )
    prices = download_adjusted_prices(
        required_tickers,
        period=period,
    )

    LOGGER.info("Calculating daily returns")
    returns = calculate_returns(prices)

    LOGGER.info("Building weighted portfolio returns")
    portfolio_returns = build_portfolio_returns(
        returns,
        portfolio,
    )

    LOGGER.info("Building factor-proxy return series")
    factor_returns = build_factor_returns(
        returns,
        FACTOR_PROXIES,
    )

    LOGGER.info("Fitting factor regression")
    result: FactorModelResult = fit_factor_model(
        portfolio_returns,
        factor_returns,
    )

    return portfolio, result


def main() -> int:
    """Run the command-line application."""

    args = parse_arguments()
    configure_logging(args.log_level)

    try:
        portfolio, result = run_factor_analysis(
            portfolio_path=args.portfolio,
            period=args.period,
        )

        print_report(portfolio, result)
        save_report(result, args.output)

        print(f"\nCSV report saved to: {args.output.resolve()}")
        return 0

    except KeyboardInterrupt:
        LOGGER.error("Analysis cancelled by user.")
        return 130

    except (ValueError, RuntimeError, OSError) as error:
        LOGGER.error("%s", error)
        return 1

    except Exception:
        LOGGER.exception("Unexpected error while running factor analysis.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
