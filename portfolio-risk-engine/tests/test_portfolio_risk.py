import numpy as np
import pandas as pd

from src.portfolio_risk_engine.risk import (
    annualized_volatility,
    build_portfolio_returns,
    expected_shortfall,
    historical_var,
    max_drawdown,
)


def test_build_portfolio_returns():
    returns = pd.DataFrame({"A": [0.10, 0.00], "B": [0.00, 0.10]})
    weights = pd.Series({"A": 0.50, "B": 0.50})
    result = build_portfolio_returns(returns, weights)
    expected = pd.Series([0.05, 0.05], name="portfolio_return")
    pd.testing.assert_series_equal(result, expected)


def test_max_drawdown():
    result = max_drawdown(pd.Series([0.10, -0.20, 0.05]))
    assert result < 0


def test_var_is_positive_loss():
    var = historical_var(pd.Series([-0.10, -0.05, -0.02, 0.01, 0.03, 0.04]))
    assert var >= 0


def test_expected_shortfall_at_least_var():
    returns = pd.Series(np.linspace(-0.20, 0.10, 100))
    assert expected_shortfall(returns) >= historical_var(returns)


def test_volatility_non_negative():
    assert annualized_volatility(pd.Series([0.01, -0.01, 0.02, -0.02])) >= 0
