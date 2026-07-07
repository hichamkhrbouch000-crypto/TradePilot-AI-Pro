import asyncio
import logging
import requests
import os
from config import DISCORD_WEBHOOK_URL

# إعداد السجلات
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

async def send_welcome_message():
    """إرسال رسالة ترحيبية للتأكد من ربط الديسكورد"""
    if DISCORD_WEBHOOK_URL:
        message = {"content": "🚀 **TradePilot AI is Online and Operational!**"}
        try:
            requests.post(DISCORD_WEBHOOK_URL, json=message)
            logger.info("تم إرسال رسالة الترحيب إلى ديسكورد بنجاح!")
        except Exception as e:
            logger.error(f"فشل إرسال رسالة الترحيب: {e}")

async def main():
    logger.info("TradePilot AI Initialized.")
    await send_welcome_message()
    
    # هنا سيعمل البوت في حلقة انتظار
    while True:
        await asyncio.sleep(3600) 

if __name__ == "__main__":
    asyncio.run(main())
