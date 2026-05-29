# Stock Portfolio Risk Dashboard

An interactive Streamlit dashboard that computes institutional-grade risk metrics for any user-defined stock portfolio using live market data pulled from Yahoo Finance.

**Live app:** [stock-portfolio-risk-dashboard-2amfedsadxghp7h3ht2ejb.streamlit.app](https://stock-portfolio-risk-dashboard-2amfedsadxghp7h3ht2ejb.streamlit.app/)

---

## Overview

Risk analytics is the language of institutional finance. This dashboard replicates the core metrics that trading desks, asset managers, and risk teams use to evaluate portfolio exposure — not just returns. Any combination of tickers and date ranges can be analyzed through the sidebar controls without touching a single line of code.

---

## Metrics

### Sharpe Ratio
Measures risk-adjusted return: how much excess return is earned per unit of volatility taken on.

```
Sharpe = (Annualized Return - Risk-Free Rate) / Annualized Volatility
```

- Annualized Return = Mean Daily Log Return × 252 trading days
- Annualized Volatility = Std Dev of Daily Log Returns × √252
- Risk-free rate defaults to **4.5%**, sourced from the Bangko Sentral ng Pilipinas (BSP) overnight lending rate

A Sharpe above 1.0 is generally considered acceptable; above 2.0 is strong. A negative Sharpe means the asset underperformed the risk-free rate.

### Maximum Drawdown (MDD)
Measures the largest peak-to-trough decline in price over the selected period, expressed as a percentage.

```
Drawdown = (Price - Running Peak) / Running Peak
MDD = Minimum value of Drawdown series
```

MDD quantifies the worst-case loss an investor would have experienced if they bought at the peak and sold at the trough. A portfolio with a -30% MDD requires a subsequent +43% gain just to break even.

### Value at Risk (VaR) — Historical Simulation
Measures the maximum expected daily loss at a given confidence level, based purely on the empirical distribution of past returns.

```
VaR (95%) = 5th percentile of daily log returns
VaR (99%) = 1st percentile of daily log returns
```

A 99% VaR of -5.77% means: there is a 99% chance that losses on any given day will not exceed 5.77%. Equivalently, a loss greater than 5.77% is expected roughly once every 100 trading days.

---

## Implementation Notes

**Log returns over simple returns:** All calculations use log returns (`np.log(P_t / P_{t-1})`) rather than simple percentage returns (`pct_change()`). Log returns are time-additive, more normally distributed, and consistent with practitioner convention for Sharpe and VaR computation.

**Caching:** The data fetch and calculation function is wrapped with `@st.cache_data`, which stores results keyed by input parameters. Adjusting the risk-free rate slider or switching display options does not trigger a redundant API call to Yahoo Finance.

**Single-ticker handling:** `df['Close']` is always coerced to a DataFrame via `pd.DataFrame()` immediately after download. Without this, a single-ticker query returns a Series, which breaks all downstream `.columns` references.

---

## Stack

`Python` `Streamlit` `yfinance` `Pandas` `NumPy`

---

## Local Setup

```bash
pip install streamlit yfinance pandas numpy
streamlit run app.py
```

The app opens at `http://localhost:8501`. Enter ticker symbols (space-separated), set a date range, adjust the risk-free rate if needed, and click **Run Analysis**.

---

## Project Context

Built as Project 1 of a self-directed summer curriculum focused on financial data science, targeting quantitative finance and investment banking applications. The project demonstrates familiarity with the risk metrics used by institutional teams and the ability to surface them through a deployed, user-facing tool.

Part of the broader portfolio at [github.com/bckenz-ai](https://github.com/bckenz-ai).
