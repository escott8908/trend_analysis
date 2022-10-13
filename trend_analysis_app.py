import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import date, timedelta

st.title('Trend Analysis Web App')

ticker_input = st.text_input("Enter Tickers (i.e.: GS, MSFT, AAPL)", 'GS, MSFT, AAPL')

period = st.text_input("Enter Period (valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max)", '1d')

# st.write(f"ticker inputs: {ticker_input}")
# st.write(f"period to extract: {period}")

@st.cache
def get_ticker_data(tickers = None, period = None):
    assert tickers is not None
    assert period is not None

    tickers = [t.strip() for t in tickers.split(',')]
    tickers_df = yf.download(tickers=tickers, period=period)
    tickers_df = tickers_df.stack().reset_index().rename(columns={'level_1':'Ticker'})

    return tickers_df

df = get_ticker_data(tickers = ticker_input, period = period)

st.write(df)

@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


csv = convert_df(df)

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='data.csv',
    mime='text/csv',
)