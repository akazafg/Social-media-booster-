import os
import time
import threading
import streamlit as st
import telebot
import ccxt
import pandas as pd

# Simple Streamlit Web Interface Layout
st.title("📈 Crypto Signal Bot Server")
st.write("Status: **Running 24/7 in the background**")
st.info("This web page keeps your background Telegram bot alive.")

# SECURE: Pulls your token secretly from the host vault instead of raw text
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
USER_CHAT_ID = "7924043459" 

SYMBOL = "BTC/USDT"
TIMEFRAME = "5m"  

def calculate_rsi(prices, period=14):
    try:
        series = pd.Series(prices)
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.iloc[-1]
    except Exception:
        return 50  

def run_bot():
    """This function runs inside a hidden background thread so the website doesn't crash."""
    if not TELEGRAM_TOKEN:
        print("ERROR: TELEGRAM_TOKEN environment variable is missing!")
        return

    bot = telebot.TeleBot(TELEGRAM_TOKEN)
    exchange = ccxt.bybit()

    # Send a quick startup alert to your Telegram app
    try:
        bot.send_message(USER_CHAT_ID, "🚀 Streamlit Server Connected! Your secure trading bot is actively monitoring the charts.")
    except Exception as e:
        print(f"Startup message failed: {e}")

    # Pure background tracking loop
    while True:
        try:
            bars = exchange.fetch_ohlcv(SYMBOL, timeframe=TIMEFRAME, limit=50)
            df = pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
            
            latest_rsi = calculate_rsi(df['close'], period=14)
            latest_price = df['close'].iloc[-1]
            
            print(f"Scanning {SYMBOL}: Price ${latest_price} | RSI: {latest_rsi:.2f}")
            
            if latest_rsi < 30:
                bot.send_message(USER_CHAT_ID, f"🟢 **UP SIGNAL (CALL)** 🟢\n\nAsset: {SYMBOL}\nPrice: ${latest_price}\nMarket is oversold ({latest_rsi:.2f}). Expecting a bounce!", parse_mode="Markdown")
                time.sleep(600) # Pause 10 mins so it doesn't spam your phone
            elif latest_rsi > 70:
                bot.send_message(USER_CHAT_ID, f"🔴 **DOWN SIGNAL (PUT)** 🔴\n\nAsset: {SYMBOL}\nPrice: ${latest_price}\nMarket is overbought ({latest_rsi:.2f}). Expecting a drop!", parse_mode="Markdown")
                time.sleep(600)
                
        except Exception as e:
            print(f"Loop error: {e}")
        
        time.sleep(30) # Check the market every 30 seconds

# CRITICAL: This fires up the bot loop in the background without locking the screen
if "bot_started" not in st.session_state:
    st.session_state.bot_started = True
    threading.Thread(target=run_bot, daemon=True).start()
