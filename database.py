def log_trade(side, symbol, price):
    # التسجيل دائماً في ملف موجود في نفس المجلد
    with open('trade_analytics.csv', 'a') as f:
        f.write(f"{side},{symbol},{price}\n")
