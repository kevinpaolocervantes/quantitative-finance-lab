# Quantitative Finance Lab

Research and implementation of quantitative models for portfolio construction, risk management, derivatives pricing, systematic investing, and market analysis.

This repository contains practical Python implementations of quantitative finance concepts. The goal is to build well-documented, reusable tools that connect financial theory with real-world portfolio analysis and market simulation.

## Objectives

- Build quantitative finance models from first principles
- Apply models to real and simulated portfolios
- Develop reusable and testable Python components
- Explore financial theory through empirical analysis
- Create a foundation for more advanced quantitative research

## Projects

### Portfolio Risk Engine

Analyze the risk profile of a portfolio using historical market data.

Planned features:

- Position and portfolio weights
- Historical returns
- Annualized volatility
- Maximum drawdown
- Correlation and covariance analysis
- Historical Value at Risk
- Expected Shortfall
- Risk contribution by position
- Concentration analysis
- Historical stress testing

### Equity Factor Models

Research and implement models used to explain asset returns.

Planned models:

- Capital Asset Pricing Model
- Fama-French Three-Factor Model
- Fama-French Five-Factor Model
- Momentum
- Quality
- Value
- Size
- Low volatility

### Portfolio Optimization

Implement portfolio construction and asset-allocation techniques.

Planned models:

- Mean-variance optimization
- Minimum-variance portfolio
- Maximum Sharpe ratio portfolio
- Efficient frontier
- Risk parity
- Black-Litterman model
- Portfolio constraints
- Rebalancing analysis

### Options Pricing

Build pricing and risk models for financial derivatives.

Planned models:

- Black-Scholes
- Binomial tree
- Monte Carlo simulation
- Implied volatility
- Option Greeks
- Volatility sensitivity analysis

### Backtesting

Develop a framework for evaluating systematic investment strategies.

Planned features:

- Historical strategy simulation
- Benchmark comparison
- Transaction costs
- Portfolio rebalancing
- Performance attribution
- Sharpe and Sortino ratios
- Drawdown analysis
- Trade-level statistics

### Market Microstructure

Explore how financial markets process and execute orders.

Planned projects:

- Limit order book simulator
- Order matching engine
- Bid-ask spread analysis
- Transaction cost analysis
- Market-impact models
- Execution algorithms
- Market-making simulator

## Repository Structure

```text
quantitative-finance-lab/
├── portfolio-risk-engine/
├── factor-models/
├── portfolio-optimization/
├── options-pricing/
├── backtesting/
├── market-microstructure/
├── shared/
├── tests/
└── README.md
