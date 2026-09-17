import numpy as np
import pandas as pd

TRADING_DAYS = 252


def build_portfolio_returns(asset_returns, weights):
    aligned = weights.reindex(asset_returns.columns)
    if aligned.isna().any():
        raise ValueError("Missing weights for one or more assets.")
    result = asset_returns.mul(aligned, axis=1).sum(axis=1)
    result.name = "portfolio_return"
    return result


def annualized_return(returns):
    if returns.empty:
        return np.nan
    years = len(returns) / TRADING_DAYS
    return (1 + returns).prod() ** (1 / years) - 1


def annualized_volatility(returns):
    return returns.std(ddof=1) * np.sqrt(TRADING_DAYS)


def sharpe_ratio(returns, risk_free_rate=0.0):
    vol = annualized_volatility(returns)
    if vol == 0 or np.isnan(vol):
        return np.nan
    return (annualized_return(returns) - risk_free_rate) / vol


def downside_deviation(returns, minimum_acceptable_return=0.0):
    target = (1 + minimum_acceptable_return) ** (1 / TRADING_DAYS) - 1
    downside = returns[returns < target] - target
    if downside.empty:
        return 0.0
    return np.sqrt(np.mean(np.square(downside))) * np.sqrt(TRADING_DAYS)


def sortino_ratio(returns, risk_free_rate=0.0):
    downside = downside_deviation(returns, risk_free_rate)
    if downside == 0 or np.isnan(downside):
        return np.nan
    return (annualized_return(returns) - risk_free_rate) / downside


def max_drawdown(returns):
    wealth = (1 + returns).cumprod()
    peaks = wealth.cummax()
    return float((wealth / peaks - 1).min())


def historical_var(returns, confidence=0.95):
    q = np.quantile(returns.dropna(), 1 - confidence)
    return max(0.0, -float(q))


def expected_shortfall(returns, confidence=0.95):
    var = historical_var(returns, confidence)
    tail = returns[returns <= -var]
    return 0.0 if tail.empty else max(0.0, -float(tail.mean()))


def calculate_risk_contributions(asset_returns, weights):
    cov = asset_returns.cov() * TRADING_DAYS
    weights = weights.reindex(cov.columns)
    w = weights.to_numpy()
    c = cov.to_numpy()

    portfolio_var = w.T @ c @ w
    portfolio_vol = np.sqrt(portfolio_var)

    if portfolio_vol == 0:
        contributions = np.zeros(len(w))
    else:
        marginal = (c @ w) / portfolio_vol
        contributions = w * marginal

    pct = contributions / portfolio_vol if portfolio_vol != 0 else np.zeros(len(w))

    return pd.DataFrame({
        "ticker": cov.columns,
        "weight": w,
        "risk_contribution": contributions,
        "risk_contribution_pct": pct,
    }).sort_values("risk_contribution_pct", ascending=False).reset_index(drop=True)


def calculate_risk_metrics(portfolio_returns, risk_free_rate=0.0, confidence=0.95):
    return {
        "annualized_return": annualized_return(portfolio_returns),
        "annualized_volatility": annualized_volatility(portfolio_returns),
        "sharpe_ratio": sharpe_ratio(portfolio_returns, risk_free_rate),
        "downside_deviation": downside_deviation(portfolio_returns, risk_free_rate),
        "sortino_ratio": sortino_ratio(portfolio_returns, risk_free_rate),
        "max_drawdown": max_drawdown(portfolio_returns),
        "historical_var": historical_var(portfolio_returns, confidence),
        "expected_shortfall": expected_shortfall(portfolio_returns, confidence),
    }
