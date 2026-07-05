import asyncio
from discord_bot.bot import run_bot
import logging

# إعداد السجلات (Logs)
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    try:
        print("🚀 جاري تشغيل بوت التداول...")
        run_bot()
    except Exception as e:
        logging.error(f"حدث خطأ أثناء التشغيل: {e}")

