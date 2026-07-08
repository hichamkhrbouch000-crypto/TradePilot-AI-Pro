import ccxt

def get_market_data():
    # الاتصال بمنصة Binance (بدون حاجة لمفاتيح في البداية لجلب البيانات العامة)
    exchange = ccxt.binance()
    
    # جلب سعر البيتكوين الحالي
    ticker = exchange.fetch_ticker('BTC/USDT')
    price = ticker['last']
    
    print(f"السعر الحالي للبيتكوين هو: {price}")
    return price

if __name__ == "__main__":
    get_market_data()
