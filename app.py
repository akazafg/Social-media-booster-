import time
import telebot
import ccxt
import pandas as pd
import pandas_ta as ta

# Your custom credentials
TELEGRAM_TOKEN = "8888466407:AAEuhd1S38dc4wUUV1_zvkr2v0i87PvVsV8
USER_CHAT_ID = "7924043459" 

bot = telebot.TeleBot(TELEGRAM_TOKEN)
exchange = ccxt.bybit()

SYMBOL = "BTC/USDT"
TIMEFRAME = "5m"  

def get_signal():
    try:
        bars = exchange.fetch_ohlcv(SYMBOL, timeframe=TIMEFRAME, limit=50)
        df = pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
        
        df['rsi'] = ta.rsi(df['close'], length=14)
        latest_rsi = df['rsi'].iloc[-1]
        latest_price = df['close'].iloc[-1]
        
        print(f"Scanning {SYMBOL}: Price ${latest_price} | RSI: {latest_rsi:.2f}")
        
        if latest_rsi < 30:
            return f"🟢 **UP SIGNAL (CALL)** 🟢\nAsset: {SYMBOL}\nPrice: ${latest_price}\nMarket is oversold. Expecting a bounce!"
        elif latest_rsi > 70:
            return f"🔴 **DOWN SIGNAL (PUT)** 🔴\nAsset: {SYMBOL}\nPrice: ${latest_price}\nMarket is overbought. Expecting a drop!"
        
        return None 
    except Exception as e:
        print(f"Error reading chart: {e}")
        return None

# Start up notification sent directly to your chat
try:
    bot.send_message(USER_CHAT_ID, "🚀 Your Trading Signal Bot is officially online and tracking the charts!")
except Exception as e:
    print(f"Could not send startup message. Did you click /start on your bot? Error: {e}")

while True:
    signal_message = get_signal()
    if signal_message:
        bot.send_message(USER_CHAT_ID, signal_message, parse_mode="Markdown")
        time.sleep(600) 
    time.sleep(30)
