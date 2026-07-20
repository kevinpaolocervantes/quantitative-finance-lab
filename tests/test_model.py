"""Tests for the equity factor model."""

import pandas as pd
import pytest

from src.equity_factor_model.model import (
    build_portfolio_returns,
    fit_factor_model,
)


def test_build_portfolio_returns_uses_weights() -> None:
    returns = pd.DataFrame(
        {
            "AAA": [0.01, 0.02],
            "BBB": [0.03, -0.01],
        }
    )

    portfolio = pd.DataFrame(
        {
            "ticker": ["AAA", "BBB"],
            "weight": [0.75, 0.25],
        }
    )

    result = build_portfolio_returns(returns, portfolio)

    assert result.iloc[0] == pytest.approx(0.015)
    assert result.iloc[1] == pytest.approx(0.0125)


def test_factor_model_requires_enough_observations() -> None:
    index = pd.date_range("2026-01-01", periods=10)

    portfolio_returns = pd.Series(
        [0.001] * 10,
        index=index,
        name="portfolio",
    )

    factor_returns = pd.DataFrame(
        {"market": [0.001] * 10},
        index=index,
    )

    with pytest.raises(ValueError, match="60 aligned daily observations"):
        fit_factor_model(portfolio_returns, factor_returns)
