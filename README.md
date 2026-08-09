<img width="2100" height="1800" alt="summary_chart" src="https://github.com/user-attachments/assets/29717647-5f82-4e44-8920-56331b08d4d5" /># Crypto Portfolio Risk Dashboard

# Overview - A risk management analysis of a 6-asset crypto portfolio (BTC, ETH, BNB, SOL, XRP, DOGE), demonstrating why standard risk models built for traditional finance (normal-distribution VaR) systematically fail on crypto assets, and how to correct for this using fat-tailed distributions and empirical validation.

# Data:
- Period: January 2021 – present
- Source: Binance API, daily log returns
- Assets: BTC-USD, ETH-USD, BNB-USD, SOL-USD, XRP-USD, DOGE-USD

# Summary Chart
<img width="2100" height="1800" alt="summary_chart" src="https://github.com/user-attachments/assets/870ac74c-b678-4bef-be7b-a9adb6b2bd80" />

# Key Findings:
Parametric (normal-distribution) VaR at the 99% confidence level understates portfolio tail risk relative to Monte Carlo with fat-tailed (Student's t) simulation — a gap confirmed not just theoretically, but empirically: a backtest shows parametric VaR was breached 67% more often than the model itself predicted (breach ratio 1.67 vs. a target of 1.0), while historical and Monte Carlo VaR remained close to correctly calibrated (1.03 and 1.27 respectively). This is critical for crypto risk management because the same normal-distribution model can look *overly conservative* at 95% confidence while *dangerously underestimating* risk at 99% confidence — the exact opposite of what a risk manager needs from a stress-testing tool. Diversification also provides less protection than expected: average pairwise correlation between the six assets rises from 0.559 in normal markets to 0.867 during genuine systemic crises (Terra/Luna and FTX collapses) — a 55% increase — meaning this portfolio behaves close to a single concentrated bet exactly when diversification is needed most.

# Methodology & Results by Section

### 1. Distribution Diagnostics
All six assets reject normality via the Jarque-Bera test (p < 0.05 for every asset). Excess kurtosis ranges from 4.05 (BTC) to 136.46 (DOGE), confirming fat tails are a structural feature of crypto returns, not a modeling artifact.

### 2. Value at Risk (VaR) — Three Methods
Historical, parametric (normal), and Monte Carlo (Student's t) VaR were compared. The normal model's error flips direction depending on confidence level: it overstates risk at 95% (due to kurtosis-inflated standard deviation) but understates tail risk by ~20% on average at 99%, exactly where risk managers care most.

### 3. Conditional VaR (Expected Shortfall)
The CVaR/VaR gap under the normal model is nearly constant across all assets (~14.7% at 99%), incorrectly implying uniform tail severity.
Monte Carlo shows this gap varies from 43% (SOL) to 82% (BNB) — tail severity is highly asset-specific and the normal model cannot capture this.

### 4. Risk-Adjusted Returns (Sharpe, Sortino, Calmar)
Sortino consistently exceeds Sharpe (up to +71% for DOGE), reflecting asymmetric, upside-skewed volatility. By traditional finance standards
(Sharpe > 1 considered "good"), this entire portfolio underperforms(0.22–0.62), highlighting that classic risk-adjusted metrics were not designed for assets with this volatility profile.

### 5. Drawdown & Underwater Analysis
All assets spent 95.9%–99.2% of the sample period below their historical peak, with max drawdowns from -70.9% (BNB) to -96.3% (SOL) — a reminder that reaching a new all-time high is a single instant, while recovery can take years.

### 6. Volatility Clustering
30-day rolling volatility shows extreme autocorrelation (0.988–0.994) across all assets, statistically confirming volatility clustering.
DOGE's volatility ranged 31.7x between its calmest and most turbulent periods — a single static volatility estimate is meaningless for position sizing in this environment.

### 7. Correlation: Calm vs. Crisis
A naive volatility-percentile proxy for "crisis" produced a misleading result (correlation appeared to *drop* in stress periods) due to DOGE's idiosyncratic noise contaminating the signal. Using known systemic crisis windows instead (Terra/Luna and FTX collapses), average pairwise correlation rises from 0.559 to 0.867 (+55%) — confirming the classic risk management principle that diversification disappears exactly when it's needed most.

### 8. Portfolio-Level VaR & Backtest
The portfolio's own historical VaR-99 (10.15%) exceeds BTC's individual VaR-99 (8.58%) despite BTC being the largest position (40%) — direct evidence that high cross-asset correlation limits diversification benefits. A backtest against actual returns confirms parametric VaR is poorly calibrated at 99% confidence (breach ratio 1.67), while historical (1.03) and Monte Carlo (1.27) methods perform close to expectations.

# Repository Structure
crypto-risk-dashboard/
├── README.md
├── requirements.txt
├── src/
│   └── risk_metrics.py
├── notebooks/
│   ├── 01_data_loader.ipynb
│   └── 02_risk_metrics.ipynb
├── data/
└── images/
    └── summary_chart.png

## How to Run
pip install -r requirements.txt
jupyter notebook notebooks/
