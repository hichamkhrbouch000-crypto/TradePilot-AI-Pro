import requests # تأكد من إضافة هذه المكتبة في requirements.txt

def send_alert(message):
    """إرسال تنبيه عبر Webhook ديسكورد"""
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if ENABLE_ALERTS and webhook_url:
        data = {"content": f"🤖 **TradePilotBot Alert**\n{message}"}
        try:
            requests.post(webhook_url, json=data)
            logger.info("تم إرسال التنبيه إلى ديسكورد")
        except Exception as e:
            logger.error(f"فشل إرسال التنبيه إلى ديسكورد: {e}")
