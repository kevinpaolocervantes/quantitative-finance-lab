# Quantitative Finance Lab

A collection of quantitative finance research projects exploring portfolio construction, risk management, asset pricing, and market microstructure.

This repository serves as a laboratory for building practical tools used by quantitative researchers, portfolio managers, and systematic investors. Each project is designed to be educational, reproducible, and applicable to real-world investing.

---

## Current Project

### Equity Factor Model

The first project in this repository estimates the historical factor exposures of an equity portfolio.

Features include:

- Portfolio construction from custom position weights
- Historical price retrieval from Yahoo Finance
- Multi-factor regression using ETF factor proxies
- Estimated exposures to:
  - Market
  - Size
  - Value
  - Momentum
  - Quality
  - Low Volatility
- Alpha estimation
- Statistical significance (p-values)
- R² and adjusted R²
- CSV report generation

Example output:

```
Market Beta:      0.999
Value Exposure:  -1.163
Quality:          0.342
Annualized Alpha: 14.71%
```

---

## Future Projects

This repository is actively evolving. Planned research projects include:

- Portfolio Risk Engine
- Portfolio Optimizer
- Options Pricing Engine
- Backtesting Framework
- Factor Investing Research
- Risk Parity Models
- Order Book Simulator
- Market Making Simulator
- Statistical Arbitrage Experiments
- Machine Learning for Asset Returns

Additional ideas will be added as the research evolves.

---

## Philosophy

The objective is not simply to recreate textbook models, but to build practical quantitative tools that improve investment decision-making while exploring modern approaches to portfolio management and financial research.

---

## Tech Stack

- Python
- NumPy
- Pandas
- Statsmodels
- yfinance
- Pytest

---

## Disclaimer

This project is intended for educational and research purposes only and should not be considered investment advice.
