import pandas as pd
import pandas_ta as ta

def calculate_indicators(ohlcv_data):
    """حساب المؤشرات الفنية باستخدام pandas_ta"""
    # تحويل البيانات إلى DataFrame (بافتراض أن البيانات بتنسيق Binance)
    df = pd.DataFrame(ohlcv_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    
    # حساب المؤشرات
    df['SMA20'] = ta.sma(df['close'], length=20)
    df['SMA50'] = ta.sma(df['close'], length=50)
    df['RSI'] = ta.rsi(df['close'], length=14)
    
    return df.iloc[-1]  # إرجاع آخر صف (آخر شمعة)

def generate_signal(indicators):
    """منطق القرار: بناءً على RSI و المتوسطات"""
    rsi = indicators['RSI']
    sma20 = indicators['SMA20']
    sma50 = indicators['SMA50']
    
    # استراتيجية بسيطة كما في كود الويب الخاص بك:
    # صعود إذا كان RSI < 40 و SMA20 > SMA50
    if rsi < 40 and sma20 > sma50:
        return "BUY"
    # هبوط إذا كان RSI > 60 و SMA20 < SMA50
    elif rsi > 60 and sma20 < sma50:
        return "SELL"
    else:
        return "HOLD"

