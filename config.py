import os

# ==================== إعدادات الحساب ====================
# تُحمل من متغيرات البيئة (Environment Variables) في Railway لأمان تام
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

# ==================== إعدادات التداول ====================
SYMBOL = "BTC/USDT"                # زوج التداول
TIMEFRAME = "15m"                  # الإطار الزمني الأفضل للتداول الفوري
TRADE_AMOUNT_USDT = 10.0           # حجم الصفقة الثابت بالدولار

# ==================== معلمات المؤشرات الفنية ====================
EMA_PERIOD = 200
RSI_PERIOD = 14
RSI_OVERBOUGHT = 60                # الحد الأقصى لمؤشر RSI للدخول
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

# ==================== إدارة المخاطر (درع الأمان) ====================
STOP_LOSS_PCT = 0.015              # 1.5% وقف خسارة
TAKE_PROFIT_PCT = 0.025            # 2.5% جني أرباح

# ==================== إعدادات النظام ====================
CHECK_INTERVAL_SECONDS = 60        # فحص السوق كل دقيقة
MAX_RETRIES = 5                    # محاولات إعادة الاتصال
RETRY_DELAY = 5                    # التأخير عند الخطأ

# تفعيل وضع الاختبار (Testnet)
# إذا أردت الحساب الحقيقي لاحقاً، اجعلها False
TEST_MODE = os.getenv("TEST_MODE", "True").lower() in ("true", "1", "yes")

# ==================== التنبيهات ====================
ENABLE_ALERTS = True
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

