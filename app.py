import time
import telebot
import ccxt
import pandas as pd
import pandas_ta as ta

# Your custom credentials
# WARNING: Replace the letters below with your full, exact token from BotFather!
TELEGRAM_TOKEN = "8888466407:AAEuhd1S38d..." 
USER_CHAT_ID = "7924043459" 

# Initialize Telegram engine & Market Data exchange
bot = telebot.TeleBot(TELEGRAM_TOKEN)
exchange = ccxt.bybit()

SYMBOL = "BTC/USDT"
TIMEFRAME = "5m"  # 5-minute chart candles

def get_signal():
    try:
        # Fetch the latest 50 candlestick bars from the market
        bars = exchange.fetch_ohlcv(SYMBOL, timeframe=TIMEFRAME, limit=50)
        df = pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
        
        # Calculate RSI safely using the append method to prevent cloud server errors
        df.ta.rsi(close='close', length=14, append=True)
        latest_rsi = df['RSI_14'].iloc[-1]
        latest_price = df['close'].iloc[-1]
        
        print(f"Scanning {SYMBOL}: Price ${latest_price} | RSI: {latest_rsi:.2f}")
        
        # Checking Signal Rules
        if latest_rsi < 30:
            return f"🟢 **UP SIGNAL (CALL)** 🟢\n\nAsset: {SYMBOL}\nPrice: ${latest_price}\nMarket is oversold ({latest_rsi:.2f}). Expecting a bounce up!"
        elif latest_rsi > 70:
            return f"🔴 **DOWN SIGNAL (PUT)** 🔴\n\nAsset: {SYMBOL}\nPrice: ${latest_price}\nMarket is overbought ({latest_rsi:.2f}). Expecting a drop down!"
        
        return None 
    except Exception as e:
        print(f"Error reading chart: {e}")
        return None

# Send a direct verification text when the server turns on
try:
    bot.send_message(USER_CHAT_ID, "🚀 Your Trading Signal Bot is officially online and tracking the charts without Streamlit!")
    print("Startup message sent to Telegram successfully!")
except Exception as e:
    print(f"Could not send startup message. Did you click /start on your bot first? Error: {e}")

# The background loop that watches the market 24/7
while True:
    signal_message = get_signal()
    if signal_message:
        bot.send_message(USER_CHAT_ID, signal_message, parse_mode="Markdown")
        print("Signal sent! Pausing for 10 minutes...")
        time.sleep(600) # Pauses for 10 minutes so it doesn't spam your phone with the same signal
        
    time.sleep(30) # Scans the lines every 30 seconds
