"""Console and CSV reporting for factor-model results."""

from pathlib import Path

import pandas as pd

from .model import FactorModelResult


FACTOR_LABELS = {
    "const": "Daily Alpha",
    "market": "Market",
    "size": "Size",
    "value": "Value",
    "momentum": "Momentum",
    "quality": "Quality",
    "low_volatility": "Low Volatility",
}


def interpret_exposure(coefficient: float, p_value: float) -> str:
    """Create a restrained interpretation of a factor coefficient."""

    significance = "statistically significant" if p_value < 0.05 else "not significant"

    if abs(coefficient) < 0.10:
        direction = "minimal"
    elif coefficient > 0:
        direction = "positive"
    else:
        direction = "negative"

    return f"{direction} exposure; {significance} at the 5% level"


def results_table(result: FactorModelResult) -> pd.DataFrame:
    """Convert model output into a readable table."""

    table = pd.DataFrame(
        {
            "coefficient": result.coefficients,
            "p_value": result.p_values,
        }
    )

    table.index = [
        FACTOR_LABELS.get(index, index.replace("_", " ").title())
        for index in table.index
    ]

    table["interpretation"] = [
        interpret_exposure(coefficient, p_value)
        for coefficient, p_value in zip(
            table["coefficient"],
            table["p_value"],
        )
    ]

    return table


def print_report(
    portfolio: pd.DataFrame,
    result: FactorModelResult,
) -> None:
    """Print a factor-exposure report to the terminal."""

    table = results_table(result)

    print()
    print("=" * 72)
    print("EQUITY PORTFOLIO FACTOR REPORT")
    print("=" * 72)

    print("\nPortfolio")
    for row in portfolio.itertuples(index=False):
        print(f"  {row.ticker:<8} {row.weight:>8.2%}")

    print("\nModel Summary")
    print(f"  Observations:       {result.observations}")
    print(f"  R-squared:          {result.r_squared:.3f}")
    print(f"  Adjusted R-squared: {result.adjusted_r_squared:.3f}")
    print(f"  Annualized alpha:   {result.annualized_alpha:.2%}")

    print("\nFactor Exposures")
    print("-" * 72)

    for factor, row in table.iterrows():
        if factor == "Daily Alpha":
            continue

        print(
            f"{factor:<18}"
            f"{row['coefficient']:>10.3f}"
            f"    p={row['p_value']:.4f}"
            f"    {row['interpretation']}"
        )

    print("\nNote")
    print(
        "  Style factors use liquid ETF proxies and are measured relative "
        "to SPY."
    )
    print(
        "  Results describe historical statistical relationships, not "
        "future returns."
    )
    print("=" * 72)


def save_report(
    result: FactorModelResult,
    output_path: str | Path,
) -> None:
    """Save the factor-exposure table as a CSV file."""

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    results_table(result).to_csv(output)
