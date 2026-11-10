# Research 001 — Equity Pairs Trading (KO / PEP)

**Status:** Stage 1 of 8 — data collection and exploratory analysis. **Research only; not a live trading system.**

## Research question
Do Coca-Cola (KO) and PepsiCo (PEP) exhibit a sufficiently stable relationship to warrant further investigation as a pairs-trading candidate?

## What this stage does
- Downloads overlapping daily, dividend/split-adjusted historical prices using Yahoo Finance via `yfinance`.
- Computes **daily return correlation** (not raw-price correlation).
- Plots both adjusted price series indexed to 100 at the first common date.
- Saves data and a chart under `outputs/` (ignored by Git).

**Interpretation:** High correlation is *not* evidence of cointegration, spread mean reversion, or profitable trading. Adjusted prices are useful for total-return comparisons; later executable spread/backtest calculations must explicitly model tradable prices, dividends, short borrow, and corporate actions.

## Run
From this directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/analyze_pair.py --start 2021-11-01 --end 2026-11-09
pytest -q
```

On Windows PowerShell, activate with `.venv\\Scripts\\Activate.ps1`.

`--end` is **exclusive**. Internet access is required for downloading data. Yahoo Finance data may be revised, incomplete, delayed, or restricted; don't treat it as institutional-quality execution data.

## Next stages (not yet implemented)
2. Estimate a hedge ratio using a training sample and test for cointegration (Engle–Granger; diagnostics and multiple-testing awareness).
3. Study spread stability, half-life, structural breaks, and out-of-sample behavior.
4. Specify entry/exit rules **without look-ahead bias**.
5. Backtest with realistic fills, commissions, slippage, borrow availability/costs, dividends, and financing.
6. Evaluate drawdown, risk-adjusted return, turnover, capacity, and robustness.
7. Forward-test using paper trading.
8. Consider limited live deployment only after risk and operational review.

## Research discipline
KO and PEP are an **illustrative hypothesis**, not a prevalidated pair. Avoid selecting pairs using future data, optimizing parameters on the test set, or inferring profitability from historical correlation alone. Short selling can create losses greater than initial capital.
