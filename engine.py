import ccxt
import time
import pandas as pd
import pandas_ta as ta
from database import log_trade
from validator import validate_signal

def fetch_rsi(exchange, symbol):
    # جلب آخر 14 شمعة لحساب RSI
    bars = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=20)
    df = pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'vol'])
    rsi = ta.rsi(df['close'], length=14)
    return rsi.iloc[-1]

def run_trading_engine():
    exchange = ccxt.kucoin()
    print("--- المحرك المتطور بدأ العمل! ---")
    log_trade("SYSTEM", "INIT", "Bot Started")
    
    while True:
        try:
            symbol = 'BTC/USDT'
            ticker = exchange.fetch_ticker(symbol)
            price = ticker['last']
            rsi_val = fetch_rsi(exchange, symbol)
            
            # عرض البيانات في الـ Logs للرقابة
            print(f"السعر: {price} | RSI: {rsi_val:.2f}")
            
            # الطلب من الـ Validator التحقق من الإشارة
            is_valid, reason = validate_signal(price, rsi_val)
            
            if is_valid:
                log_trade("BUY", symbol, price)
            else:
                print(f"الإشارة مرفوضة: {reason}")
            
            time.sleep(60)
        except Exception as e:
            print(f"حدث خطأ: {e}")
            time.sleep(60)

if __name__ == "__main__":
    run_trading_engine()
