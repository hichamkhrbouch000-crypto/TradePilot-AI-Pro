import pandas as pd
import pandas_ta as ta

def calculate_risk_metrics(df, current_price, balance=1000):
    # 1. حساب ATR للتقلبات (14 يوم)
    atr = ta.atr(df['high'], df['low'], df['close'], length=14).iloc[-1]
    
    # 2. إعدادات المخاطرة
    stop_loss = current_price - (atr * 2) # وقف خسارة متحرك بضعف التقلب
    take_profit = current_price + (atr * 4) # هدف ربح بنسبة 1:2
    
    risk_amount = current_price - stop_loss
    reward_amount = take_profit - current_price
    rr_ratio = reward_amount / risk_amount
    
    # 3. حجم المركز (Position Sizing)
    position_size = (balance * 0.5) / current_price 
    
    return {
        "entry": current_price,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "size": position_size,
        "rr_ratio": rr_ratio,
        "is_valid": rr_ratio >= 2.0 # شرط قبول الصفقة: R:R لا يقل عن 2
    }

