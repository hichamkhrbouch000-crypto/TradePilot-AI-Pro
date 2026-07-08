import datetime

def log_trade(action, symbol, price):
    # فتح ملف نصي وإضافة الصفقة الجديدة فيه
    with open("trades.txt", "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{timestamp} | {action} | {symbol} | Price: {price}\n")
    print(f"تم تسجيل العملية: {action} لـ {symbol} بسعر {price}")

