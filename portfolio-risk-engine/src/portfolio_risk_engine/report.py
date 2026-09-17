from pathlib import Path
import pandas as pd


def print_report(metrics, risk_contributions, confidence):
    print("\nPORTFOLIO RISK REPORT")
    print("=" * 50)
    print(f"Annualized Return:      {metrics['annualized_return']:.2%}")
    print(f"Annualized Volatility:  {metrics['annualized_volatility']:.2%}")
    print(f"Sharpe Ratio:           {metrics['sharpe_ratio']:.3f}")
    print(f"Sortino Ratio:          {metrics['sortino_ratio']:.3f}")
    print(f"Downside Deviation:     {metrics['downside_deviation']:.2%}")
    print(f"Maximum Drawdown:       {metrics['max_drawdown']:.2%}")
    print(f"{confidence:.0%} Daily VaR:         {metrics['historical_var']:.2%}")
    print(f"{confidence:.0%} Expected Shortfall:{metrics['expected_shortfall']:.2%}")
    print("\nRISK CONTRIBUTION")
    print("-" * 50)
    for _, row in risk_contributions.iterrows():
        print(f"{row['ticker']:<8} Weight: {row['weight']:>7.2%} | Risk Contribution: {row['risk_contribution_pct']:>7.2%}")


def save_report(metrics, risk_contributions, output_path):
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    pd.DataFrame(
        [{"metric": k, "value": v} for k, v in metrics.items()]
    ).to_csv(output.with_name(f"{output.stem}_metrics.csv"), index=False)

    risk_contributions.to_csv(
        output.with_name(f"{output.stem}_risk_contributions.csv"),
        index=False,
    )
