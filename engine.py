import ccxt
import time

def run_engine():
    # الاتصال بمنصة Binance
    exchange = ccxt.binance()
    print("المحرك يعمل الآن ويراقب السوق...")
    
    while True:
        try:
            # جلب السعر
            ticker = exchange.fetch_ticker('BTC/USDT')
            price = ticker['last']
            print(f"السعر الحالي لـ BTC/USDT هو: {price}")
            
            # هنا يمكنك إضافة منطق التحليل الخاص بك
            # مثال: إذا كان السعر أقل من 60000، افعل شيئاً
            
            time.sleep(60) # انتظر دقيقة قبل الفحص التالي
        except Exception as e:
            print(f"حدث خطأ: {e}")
            time.sleep(60)

if __name__ == "__main__":
    run_engine()
