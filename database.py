import datetime
import requests
import csv
import os

# رابط الديسكورد الخاص بك
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1524031878888161491/ZdJI5aWWngHeQcXfPlwjHTbyLJw_-7KieFaFFPf3eTggj3Y7aWIo6cxKrGeC8NKudz9_"

# دالة إرسال تنبيهات ديسكورد
def log_trade(action, symbol, price):
    message = f"🚀 صفقة جديدة: {action} على {symbol} بالسعر {price}"
    data = {"content": message}
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=data)
    except Exception as e:
        print(f"خطأ في إرسال التنبيه: {e}")

# دالة تسجيل القرارات (للملف التحليلي)
def log_decision(decision_data):
    file_name = "trade_analytics.csv"
    file_exists = os.path.isfile(file_name)
    
    with open(file_name, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=decision_data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(decision_data)
