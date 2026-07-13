import time
import telebot
import ccxt
import pandas as pd

# Your custom credentials
TELEGRAM_TOKEN = "8888466407:AAEuhd1S38d..." # Keep your full token here!
USER_CHAT_ID = "7924043459" 

bot = telebot.TeleBot(TELEGRAM_TOKEN)
exchange = ccxt.bybit()

SYMBOL = "BTC/USDT"
TIMEFRAME = "5m"  

def calculate_rsi(prices, period=14):
    """Calculates pure RSI math manually so the server never crashes."""
    try:
        series = pd.Series(prices)
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.iloc[-1]
    except Exception:
        return 50  # Default to neutral if math fails

def get_signal():
    try:
        bars = exchange.fetch_ohlcv(SYMBOL, timeframe=TIMEFRAME, limit=50)
        df = pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
        
        # Calculate RSI cleanly
        latest_rsi = calculate_rsi(df['close'], period=14)
        latest_price = df['close'].iloc[-1]
        
        print(f"Scanning {SYMBOL}: Price ${latest_price} | RSI: {latest_rsi:.2f}")
        
        if latest_rsi < 30:
            return f"🟢 **UP SIGNAL (CALL)** 🟢\n\nAsset: {SYMBOL}\nPrice: ${latest_price}\nMarket is oversold ({latest_rsi:.2f}). Expecting a bounce!"
        elif latest_rsi > 70:
            return f"🔴 **DOWN SIGNAL (PUT)** 🔴\n\nAsset: {SYMBOL}\nPrice: ${latest_price}\nMarket is overbought ({latest_rsi:.2f}). Expecting a drop!"
        
        return None 
    except Exception as e:
        print(f"Error reading chart: {e}")
        return None

# Start up notification
try:
    bot.send_message(USER_CHAT_ID, "🚀 Your Trading Signal Bot is officially online and tracking the charts without Streamlit!")
    print("Startup message sent successfully!")
except Exception as e:
    print(f"Could not send startup message: {e}")

while True:
    signal_message = get_signal()
    if signal_message:
        bot.send_message(USER_CHAT_ID, signal_message, parse_mode="Markdown")
        time.sleep(600) 
    time.sleep(30)
