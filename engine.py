import ccxt
import time
from database import log_trade

def run_trading_engine():
    # استخدام KuCoin لتجاوز قيود الموقع الجغرافي
    exchange = ccxt.kucoin()
    print("--- المحرك النشط بدأ العمل! ---")
    
    # رسالة تجريبية للتأكد من ربط الديسكورد يعمل فور التشغيل
    log_trade("TEST", "SYSTEM", "0.0") 
    
    while True:
        try:
            ticker = exchange.fetch_ticker('BTC/USDT')
            price = ticker['last']
            print(f"السعر الحالي لـ BTC/USDT هو: {price}")
            
            # شرط الشراء (مرفوع لـ 63000 لضمان وصول التنبيه)
            if price < 63000:
                log_trade("BUY", "BTC/USDT", price)
            
            # انتظار دقيقة قبل الفحص التالي
            time.sleep(60)
            
        except Exception as e:
            print(f"حدث خطأ: {e}")
            time.sleep(60)

if __name__ == "__main__":
    run_trading_engine()
