import os
from dotenv import load_dotenv

load_dotenv()

# إعدادات عامة
SYMBOL = os.getenv("SYMBOL", "BTC/USDT")
TIMEFRAME = os.getenv("TIMEFRAME", "1h")
TEST_MODE = os.getenv("TEST_MODE", "True") == "True"

# المفاتيح السرية
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# إعدادات التداول
POSITION_SIZE_PERCENT = 0.5  # 50% من الرصيد

