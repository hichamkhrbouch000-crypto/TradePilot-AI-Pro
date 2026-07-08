import time

# متغيرات الحماية
last_trade_time = 0
COOLDOWN_PERIOD = 3600  # 3600 ثانية = ساعة كاملة بين الصفقات

def validate_signal(current_price, rsi_value):
    global last_trade_time
    
    # 1. فلتر التكرار (Cooldown)
    if time.time() - last_trade_time < COOLDOWN_PERIOD:
        return False, "في فترة تبريد (Cooldown)"
    
    # 2. فلتر RSI (منطقة التشبع)
    # لا نشتري إذا كان السوق مشبعاً جداً بالشراء (RSI > 70)
    if rsi_value > 70:
        return False, f"RSI مرتفع جداً: {rsi_value:.2f}"
    
    # إذا تجاوزت الإشارة جميع الفلاتر
    last_trade_time = time.time()
    return True, "إشارة مقبولة"

