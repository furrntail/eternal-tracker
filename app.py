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
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    for item in soup.select('div.dbsr')[:5]:
        title = item.select_one('div.JheGif.nDgy9d').text
        link = item.a['href']
        st.markdown(f"🔗 [{title}]({link})")

def check_signal():
    st.subheader("💹 Buy/Sell Signal")
    stock_symbol = "ETERNAL.NS"  # Updated ticker symbol
    data = yf.download(stock_symbol, period='2mo', interval='1d')
    if data.empty:
        st.error("⚠️ No stock data found. Check symbol.")
        return

    data['MA20'] = data['Close'].rolling(window=20).mean()
    latest = data.iloc[-1]
    previous = data.iloc[-2]

    st.write(f"💰 Latest Price: ₹{latest['Close']:.2f}")
    st.write(f"📊 20-Day MA: ₹{latest['MA20']:.2f}")

    if previous['Close'] < previous['MA20'] and latest['Close'] > latest['MA20']:
        st.success("✅ BUY SIGNAL")
    elif previous['Close'] > previous['MA20'] and latest['Close'] < latest['MA20']:
        st.error("🚨 SELL SIGNAL")
    else:
        st.info("⏳ HOLD")

get_eternal_news()
check_signal()

