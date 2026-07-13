import time
import ccxt
import pandas as pd

# 1. Connect to your exchange securely via API
exchange = ccxt.binance({
    'apiKey': 'YOUR_API_KEY',
    'secret': 'YOUR_SECRET_KEY',
})

SYMBOL = 'BTC/USDT'
TRADE_AMOUNT = 0.001 

def get_market_data():
    # Fetch recent price candles (OHLCV)
    candles = exchange.fetch_ohlcv(SYMBOL, timeframe='15m', limit=50)
    df = pd.DataFrame(candles, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
    return df

def trading_strategy(df):
    # Example: Simple moving average strategy
    short_ma = df['close'].rolling(window=10).mean().iloc[-1]
    long_ma = df['close'].rolling(window=30).mean().iloc[-1]
    
    if short_ma > long_ma:
        return 'BUY'
    elif short_ma < long_ma:
        return 'SELL'
    return 'HOLD'

# 2. The Execution Loop
while True:
    try:
        data = get_market_data()
        signal = trading_strategy(data)
        
        if signal == 'BUY':
            print("Trend is Up! Placing Buy Order...")
            # exchange.create_market_buy_order(SYMBOL, TRADE_AMOUNT)
        elif signal == 'SELL':
            print("Trend is Down! Placing Sell Order...")
            # exchange.create_market_sell_order(SYMBOL, TRADE_AMOUNT)
            
    except Exception as e:
        print(f"Error encountered: {e}")
        
    time.sleep(900) # Wait 15 minutes before checking next candle
