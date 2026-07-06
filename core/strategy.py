import pandas as pd
import pandas_ta as ta

def calculate_indicators(ohlcv_data):
    """حساب المؤشرات الفنية باستخدام pandas_ta"""
    df = pd.DataFrame(ohlcv_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    
    # حساب المؤشرات
    df['SMA20'] = ta.sma(df['close'], length=20)
    df['SMA50'] = ta.sma(df['close'], length=50)
    df['RSI'] = ta.rsi(df['close'], length=14)
    
    return df.iloc[-1]

def generate_signal(indicators):
    """منطق القرار"""
    rsi = indicators['RSI']
    sma20 = indicators['SMA20']
    sma50 = indicators['SMA50']
    
    if rsi < 40 and sma20 > sma50:
        return "BUY"
    elif rsi > 60 and sma20 < sma50:
        return "SELL"
    else:
        return "HOLD"
