import datetime
import requests

# الرابط الخاص بك مدمج الآن في الكود
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1524031878888161491/ZdJI5aWWngHeQcXfPlwjHTbyLJw_-7KieFaFFPf3eTggj3Y7aWIo6cxKrGeC8NKudz9_"

def log_trade(action, symbol, price):
    # 1. تسجيل في الملف النصي كنسخة احتياطية
    with open("trades.txt", "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{timestamp} | {action} | {symbol} | Price: {price}\n")
    
    # 2. إرسال رسالة إلى Discord
    message = f"🚀 صفقة جديدة: {action} على {symbol} بالسعر {price}"
    data = {"content": message}
    
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=data)
        print(f"تم إرسال التنبيه إلى Discord: {action}")
    except Exception as e:
        print(f"خطأ في إرسال التنبيه: {e}")
