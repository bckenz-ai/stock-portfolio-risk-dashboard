import yfinance as yf
import pandas as pd
import numpy as np
# import matplotlib as mpl
import seaborn as sns
import streamlit as st

# 1. Page Configuration
st.set_page_config(page_title="Stock Portfolio Risk Dashboard", layout="wide")

st.title("Stock Sharpe Ratio & Max Drawdown Calculator")
st.write("This app downloads historical data and calculates the annualized Sharpe Ratio, Max Drawdown (MDD), and Value-at-Risk (VaR).")

# 2. Sidebar Input Elements
st.sidebar.header("User Controls")
ticker_input = st.sidebar.text_input("Enter Ticker Symbols (space-separated):", value="AAPL MSFT GOOG")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2025-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2026-01-01"))
risk_free_rate = st.sidebar.number_input("Risk-Free Rate (e.g. 0.04 for 4%)", value=0.0)

# 3. Data Processing Wrappers
@st.cache_data
def fetch_and_calculate(tickers, start, end, rf):
    df = yf.download(tickers, start=start, end=end)
    prices = df["Close"]
    prices = pd.DataFrame(prices)
    
    # Calculate daily returns
    daily_returns = np.log(prices / prices.shift(1))

    # Sharpe Ratio Calculation
    # Annualized Return = Mean Daily Return * 252 trading days
    # Annualized Volatility = Std Dev Daily Return * sqrt(252)
    mean_return = daily_returns.mean(axis=0)
    volatility = daily_returns.std(axis=0)
    
    annualized_return = mean_return * 252
    annualized_vol = volatility * np.sqrt(252)
    
    sharpe = (annualized_return - rf) / annualized_vol
    
    # Calculate Drawdown
    peaks = prices.cummax()
    drawdowns = (prices - peaks) / peaks
    max_dd = drawdowns.min() * 100

    # Historical VaR (negative = loss)
    var_95 = daily_returns.quantile(0.05)   # 5th percentile = 95% VaR
    var_99 = daily_returns.quantile(0.01)   # 1st percentile = 99% VaR
    
    return prices, sharpe, drawdowns, max_dd, var_95, var_99

# 4. App Execution Logic
if st.sidebar.button("Run Analysis"):
    with st.spinner("Downloading data from Yahoo Finance..."):
        try:
            # Execute logic
            prices, sharpe, drawdowns, max_dd, var_95, var_99 = fetch_and_calculate(ticker_input, start_date, end_date, risk_free_rate)
            
            # 5. Display Summary KPI Cards for the Tickers
            st.subheader("Key Performance Metrics Summary")
            kpi_cols = st.columns(len(prices.columns))
            for i, ticker in enumerate(prices.columns):
                with kpi_cols[i]:
                    st.metric(
                        label=f"{ticker}", 
                        value=f"Sharpe: {sharpe[ticker]:.2f}", 
                        delta=f"Max DD: {max_dd[ticker]:.2f}%",
                        delta_color="inverse" # Keeps negative numbers red
                    )
            
            st.markdown("---")
            
            # Split screen into four columns for detailed data
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.subheader("Sharpe Ratio Table")
                # Format dataframe for presentation
                st.dataframe(sharpe.to_frame(name="Sharpe Ratio").style.format("{:.3f}"))

            with col2:
                st.subheader("Maximum Drawdowns")
                # Format dataframe for presentation
                st.dataframe(max_dd.to_frame(name="Max Drawdown (%)").style.format("{:.2f}%"))
                
            with col3:
                st.subheader("Historical Closing Prices")
                st.line_chart(prices)

            with col4:
                st.subheader("Value at Risk (Daily)")
                var_df = pd.DataFrame({
                    "VaR 95%": (var_95 * 100).round(2),
                    "VaR 99%": (var_99 * 100).round(2)
                })
                st.dataframe(var_df.style.format("{:.2f}%"))
                
            # Full-width display for drawdowns over time
            st.subheader("Drawdown Over Time")
            st.line_chart(drawdowns)
            
        except Exception as e:
            st.error(f"Error processing data. Please check ticker symbols. Details: {e}")
else:
    st.info("Click **Run Analysis** in the sidebar to load the data.")