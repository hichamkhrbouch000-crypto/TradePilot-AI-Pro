import ccxt
import time

def run_trading_engine():
    # الاتصال بمنصة Binance لجلب البيانات العامة
    exchange = ccxt.binance()
    print("--- المحرك النشط بدأ العمل! ---")
    
    while True:
        try:
            # جلب سعر البيتكوين
            ticker = exchange.fetch_ticker('BTC/USDT')
            price = ticker['last']
            
            # طباعة السعر في السجلات (Logs)
            print(f"السعر الحالي لـ BTC/USDT هو: {price}")
            
            # هنا سنضع منطق التحليل لاحقاً
            # مثال: إذا انخفض السعر عن X، سنقوم بالتسجيل في المحفظة
            
            # ننتظر 60 ثانية قبل التحديث القادم
            time.sleep(60)
            
        except Exception as e:
            print(f"حدث خطأ في المحرك: {e}")
            time.sleep(60)

if __name__ == "__main__":
    run_trading_engine()
