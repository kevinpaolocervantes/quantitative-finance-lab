# Quantitative Finance Lab

A collection of open-source quantitative finance research projects focused on portfolio construction, risk management, asset pricing, derivatives, and systematic investing.

This repository serves as a research laboratory for developing practical quantitative models used by quantitative researchers, portfolio managers, traders, and financial engineers. Each project emphasizes reproducible research, mathematical rigor, and production-quality Python implementations.

---

# Current Projects

## Equity Factor Model

Estimate the historical factor exposures of an equity portfolio using multi-factor regression analysis.

### Features

- Portfolio construction from custom position weights
- Historical price retrieval using Yahoo Finance
- Multi-factor regression using ETF factor proxies
- Estimated exposures to:
  - Market
  - Size
  - Value
  - Momentum
  - Quality
  - Low Volatility
- Annualized alpha estimation
- Statistical significance testing (p-values)
- R² and Adjusted R²
- CSV report generation

### Example Output

```text
Factor Exposures

Market Beta        0.999
Size               0.218
Value             -1.163
Momentum           0.447
Quality            0.342
Low Volatility    -0.116

Annualized Alpha  14.71%
Adjusted R²        0.82
```

---

## Portfolio Risk Engine

Analyze the historical risk characteristics of a custom equity portfolio.

### Features

- Annualized return
- Annualized volatility
- Sharpe ratio
- Sortino ratio
- Downside deviation
- Maximum drawdown
- Historical Value-at-Risk (VaR)
- Expected Shortfall (CVaR)
- Asset-level risk contribution
- CSV report generation

### Example Output

```text
PORTFOLIO RISK REPORT

Annualized Return:       18.42%
Annualized Volatility:   24.17%
Sharpe Ratio:             0.60
Sortino Ratio:            0.89
Maximum Drawdown:       -28.41%
95% Daily VaR:            2.31%
95% Expected Shortfall:   3.47%
```

---

# Research Roadmap

The long-term objective is to build a comprehensive open-source quantitative finance toolkit.

## Portfolio Analytics

- ✅ Equity Factor Model
- ✅ Portfolio Risk Engine
- Portfolio Optimizer
- Performance Attribution
- Risk Parity Portfolio
- Black-Litterman Allocation

## Derivatives

- Black-Scholes Pricing Engine
- Binomial Options Pricing
- Greeks Calculator
- Volatility Surface Modeling
- Monte Carlo Option Pricing

## Market Microstructure

- Limit Order Book Simulator
- Market Making Simulator
- Execution Cost Analysis
- Liquidity Modeling

## Quantitative Research

- Statistical Arbitrage
- Factor Investing Research
- Time Series Forecasting
- Regime Detection
- Machine Learning for Asset Returns
- Alternative Data Research

## Risk Management

- Stress Testing Framework
- Scenario Analysis
- Credit Risk Models
- Portfolio Monte Carlo Simulation
- Tail Risk Analytics

---

# Design Principles

Every project in this repository is built around five principles:

- Mathematical correctness
- Production-quality Python
- Reproducible research
- Modular architecture
- Practical application to institutional investing

---

# Technology Stack

- Python
- NumPy
- Pandas
- SciPy
- Statsmodels
- scikit-learn
- yfinance
- Matplotlib
- Pytest

---

# Long-Term Vision

Quantitative Finance Lab is intended to evolve into a comprehensive library of institutional-grade quantitative finance models. Rather than isolated notebooks or scripts, each project is designed as a reusable research module that can be combined with others to study portfolio construction, risk, pricing, execution, and systematic investment strategies.

---

# Disclaimer

This repository is intended for educational and research purposes only. Nothing contained herein constitutes investment, financial, or legal advice. Past performance, model outputs, and simulated results do not guarantee future outcomes.
