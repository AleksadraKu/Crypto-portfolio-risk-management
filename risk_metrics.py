"""
risk_metrics.py

Reusable functions for portfolio risk analysis:
VaR, CVaR, risk-adjusted returns, drawdown metrics.
"""

import numpy as np
import pandas as pd
from scipy.stats import norm, t as t_dist


ANNUALIZATION = 365  # crypto trades every day, unlike stocks (252 days)


# ============================================================
# VaR — three methods
# ============================================================

def historical_var(returns, confidence=0.95):
    """Historical VaR: empirical percentile of the return distribution."""
    return -np.percentile(returns, (1 - confidence) * 100)


def parametric_var(returns, confidence=0.95):
    """Parametric (variance-covariance) VaR assuming normal distribution."""
    mu = returns.mean()
    sigma = returns.std()
    z_score = norm.ppf(1 - confidence)
    return -(mu + z_score * sigma)


def monte_carlo_var(returns, confidence=0.95, n_simulations=100_000, random_seed=42):
    """Monte Carlo VaR using a fitted Student's t-distribution."""
    params = t_dist.fit(returns)
    df, loc, scale = params

    rng = np.random.default_rng(random_seed)
    simulated_returns = t_dist.rvs(df, loc=loc, scale=scale,
                                     size=n_simulations, random_state=rng)

    return -np.percentile(simulated_returns, (1 - confidence) * 100)


# ============================================================
# CVaR — three methods
# ============================================================

def historical_cvar(returns, confidence=0.95):
    """Historical CVaR (Expected Shortfall)."""
    var = historical_var(returns, confidence)
    tail_losses = returns[returns <= -var]
    return -tail_losses.mean()


def parametric_cvar(returns, confidence=0.95):
    """Parametric CVaR assuming normal distribution (closed-form)."""
    mu = returns.mean()
    sigma = returns.std()
    z = norm.ppf(1 - confidence)
    cvar = mu - sigma * norm.pdf(z) / (1 - confidence)
    return -cvar


def monte_carlo_cvar(returns, confidence=0.95, n_simulations=100_000, random_seed=42):
    """Monte Carlo CVaR using a fitted Student's t-distribution."""
    params = t_dist.fit(returns)
    df, loc, scale = params

    rng = np.random.default_rng(random_seed)
    simulated_returns = t_dist.rvs(df, loc=loc, scale=scale,
                                     size=n_simulations, random_state=rng)

    var_threshold = np.percentile(simulated_returns, (1 - confidence) * 100)
    tail_losses = simulated_returns[simulated_returns <= var_threshold]
    return -tail_losses.mean()


# ============================================================
# Risk-adjusted return metrics
# ============================================================

def sharpe_ratio(returns, rf_annual=0.0):
    """Sharpe ratio: return per unit of total volatility."""
    rf_daily = rf_annual / ANNUALIZATION
    excess = returns - rf_daily
    return excess.mean() / excess.std() * np.sqrt(ANNUALIZATION)


def sortino_ratio(returns, rf_annual=0.0):
    """Sortino ratio: return per unit of downside volatility only."""
    rf_daily = rf_annual / ANNUALIZATION
    excess = returns - rf_daily
    downside_returns = excess[excess < 0]
    downside_std = downside_returns.std()
    return excess.mean() / downside_std * np.sqrt(ANNUALIZATION)


def max_drawdown(price_series):
    """Returns (max_drawdown_value, drawdown_series)."""
    cumulative_max = price_series.cummax()
    drawdown = price_series / cumulative_max - 1
    return drawdown.min(), drawdown


def calmar_ratio(log_returns_series, price_series):
    """Calmar ratio: annualized return / max drawdown."""
    n_days = len(log_returns_series)
    total_log_return = log_returns_series.sum()
    annualized_return = np.exp(total_log_return * ANNUALIZATION / n_days) - 1
    mdd, _ = max_drawdown(price_series)
    return annualized_return / abs(mdd)


def underwater_curve(price_series):
    """% below the running historical peak at each point in time."""
    cumulative_max = price_series.cummax()
    return price_series / cumulative_max - 1


def pct_time_underwater(price_series, threshold=-0.01):
    """% of days the asset spent below its historical peak beyond threshold."""
    uw = underwater_curve(price_series)
    return (uw < threshold).mean()


# ============================================================
# VaR backtesting
# ============================================================

def var_breach_test(returns, var_value, confidence):
    """Compare actual VaR breaches vs expected breaches."""
    breaches = (returns < -var_value).sum()
    expected_breaches = len(returns) * (1 - confidence)
    return breaches, round(expected_breaches, 1)
