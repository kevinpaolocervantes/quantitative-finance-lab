"""Portfolio construction and factor-regression functions."""

from dataclasses import dataclass

import pandas as pd
import statsmodels.api as sm


@dataclass(frozen=True)
class FactorModelResult:
    """Container for factor-model outputs."""

    coefficients: pd.Series
    p_values: pd.Series
    r_squared: float
    adjusted_r_squared: float
    observations: int
    annualized_alpha: float


def build_portfolio_returns(
    asset_returns: pd.DataFrame,
    portfolio: pd.DataFrame,
) -> pd.Series:
    """Create a daily portfolio-return series from fixed target weights."""

    tickers = portfolio["ticker"].tolist()
    missing = sorted(set(tickers).difference(asset_returns.columns))

    if missing:
        raise ValueError(
            f"Asset returns are missing portfolio tickers: {', '.join(missing)}"
        )

    weights = portfolio.set_index("ticker")["weight"].reindex(tickers)
    aligned_returns = asset_returns[tickers].dropna()

    portfolio_returns = aligned_returns.mul(weights, axis=1).sum(axis=1)
    portfolio_returns.name = "portfolio"

    return portfolio_returns


def build_factor_returns(
    proxy_returns: pd.DataFrame,
    proxy_map: dict[str, str],
) -> pd.DataFrame:
    """
    Build relative factor-return series using ETF proxies.

    Each style proxy is measured relative to the broad market proxy.
    This reduces the amount of general market movement embedded in each
    style factor.
    """

    market_ticker = proxy_map["market"]

    if market_ticker not in proxy_returns.columns:
        raise ValueError(f"Missing market proxy: {market_ticker}")

    factors = pd.DataFrame(index=proxy_returns.index)
    factors["market"] = proxy_returns[market_ticker]

    for factor_name, ticker in proxy_map.items():
        if factor_name == "market":
            continue

        if ticker not in proxy_returns.columns:
            raise ValueError(f"Missing proxy ticker for {factor_name}: {ticker}")

        factors[factor_name] = (
            proxy_returns[ticker] - proxy_returns[market_ticker]
        )

    return factors.dropna()


def fit_factor_model(
    portfolio_returns: pd.Series,
    factor_returns: pd.DataFrame,
) -> FactorModelResult:
    """Estimate portfolio factor exposures using ordinary least squares."""

    combined = pd.concat(
        [portfolio_returns.rename("portfolio"), factor_returns],
        axis=1,
        join="inner",
    ).dropna()

    if len(combined) < 60:
        raise ValueError(
            "At least 60 aligned daily observations are required."
        )

    dependent_variable = combined["portfolio"]
    independent_variables = sm.add_constant(
        combined.drop(columns="portfolio"),
        has_constant="add",
    )

    fitted_model = sm.OLS(
        dependent_variable,
        independent_variables,
    ).fit()

    annualized_alpha = float(fitted_model.params["const"] * 252)

    return FactorModelResult(
        coefficients=fitted_model.params,
        p_values=fitted_model.pvalues,
        r_squared=float(fitted_model.rsquared),
        adjusted_r_squared=float(fitted_model.rsquared_adj),
        observations=int(fitted_model.nobs),
        annualized_alpha=annualized_alpha,
    )
