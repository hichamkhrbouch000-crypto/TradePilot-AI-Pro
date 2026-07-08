import ccxt
import time
from database import log_trade # استيراد دالة التسجيل

def run_trading_engine():
    exchange = ccxt.kucoin() # استخدمنا KuCoin لتجنب القيود
    print("--- المحرك النشط بدأ العمل! ---")
    
    while True:
        try:
            ticker = exchange.fetch_ticker('BTC/USDT')
            price = ticker['last']
            print(f"السعر الحالي لـ BTC/USDT هو: {price}")
            
            # --- منطق بسيط للتجربة ---
            # لنقل إننا سنشتري إذا كان السعر أقل من 62000 كمحاكاة
            if price < 62000:
                log_trade("BUY", "BTC/USDT", price)
            
            time.sleep(60)
        except Exception as e:
            print(f"حدث خطأ: {e}")
            time.sleep(60)

if __name__ == "__main__":
    run_trading_engine()
