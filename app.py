import streamlit as st
import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

st.set_page_config(page_title="Eternal Ltd Stock Tracker", layout="wide")

st.title("📈 Eternal Ltd Stock Tracker")
st.write(f"Date: {datetime.today().strftime('%Y-%m-%d')}")

def get_eternal_news():
    st.subheader("📰 Latest News")
    query = "Eternal Ltd stock India"
    url = f"https://www.google.com/search?q={query}&tbm=nws"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        news_items = soup.select('div.dbsr')
        if not news_items:
            st.write("No news found.")
            return
        for item in news_items[:5]:
            title = item.select_one('div.JheGif.nDgy9d').text
            link = item.a['href']
            st.markdown(f"🔗 [{title}]({link})")
    except Exception as e:
        st.error(f"Error fetching news: {e}")

def check_signal():
    st.subheader("💹 Buy/Sell Signal")
    stock_symbol = "ETERNAL.NS"  # Correct ticker symbol on NSE
    try:
        data = yf.download(stock_symbol, period='2mo', interval='1d')
        if data.empty:
            st.error("⚠️ No stock data found. Check symbol or try later.")
            return

        data['MA20'] = data['Close'].rolling(window=20).mean()

        latest = data.iloc[-1]
        previous = data.iloc[-2]

        latest_close = latest['Close']
        latest_ma20 = latest['MA20']
        previous_close = previous['Close']
        previous_ma20 = previous['MA20']

        if pd.isna(latest_close) or pd.isna(latest_ma20):
            st.error("⚠️ Incomplete data for analysis.")
            return

        st.write(f"💰 Latest Price: ₹{latest_close:.2f}")
        st.write(f"📊 20-Day MA: ₹{latest_ma20:.2f}")

        if (previous_close < previous_ma20) and (latest_close > latest_ma20):
            st.success("✅ BUY SIGNAL")
        elif (previous_close > previous_ma20) and (latest_close < latest_ma20):
            st.error("🚨 SELL SIGNAL")
        else:
            st.info("⏳ HOLD")
    except Exception as e:
        st.error(f"Error fetching stock data: {e}")

get_eternal_news()
check_signal()
