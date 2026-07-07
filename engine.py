import ccxt
import pandas as pd
import pandas_ta as ta
import time
import logging
import os
import requests
from config import *

# إعداد السجلات
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def send_alert(message):
    """إرسال تنبيه عبر Webhook ديسكورد"""
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if ENABLE_ALERTS and webhook_url:
        data = {"content": f"🤖 **TradePilotBot Alert**\n{message}"}
        try:
            requests.post(webhook_url, json=data)
            logger.info("تم إرسال التنبيه إلى ديسكورد")
        except Exception as e:
            logger.error(f"فشل إرسال التنبيه: {e}")

class TradingBot:
    def __init__(self):
        # هنا ستغير 'binance' لاحقاً للمنصة الجديدة التي ستختارها
        self.exchange = ccxt.binance({
            'apiKey': API_KEY,
            'secret': API_SECRET,
            'enableRateLimit': True,
        })
        if TEST_MODE:
            self.exchange.set_sandbox_mode(True)
        self.exchange.load_markets()
        self.market = self.exchange.market(SYMBOL)
        self.min_notional = self.market['limits']['cost']['min']
        logger.info("تم تهيئة البوت بنجاح")

    def fetch_ohlcv(self):
        ohlcv = self.exchange.fetch_ohlcv(SYMBOL, TIMEFRAME, limit=100)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        return df

    def run(self):
        logger.info("البوت يعمل الآن...")
        while True:
            try:
                df = self.fetch_ohlcv()
                # هنا سيتم وضع منطق الاستراتيجية لاحقاً
                logger.info(f"فحص السوق... السعر الحالي: {df['close'].iloc[-1]}")
                time.sleep(CHECK_INTERVAL_SECONDS)
            except Exception as e:
                logger.error(f"خطأ: {e}")
                time.sleep(10)

if __name__ == "__main__":
    bot = TradingBot()
    bot.run()
