import ccxt.async_support as ccxt
import logging
from config.settings import API_KEY, SECRET, SYMBOL

# إعداد نظام تسجيل الأخطاء
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TradingEngine:
    def __init__(self):
        # إعداد الاتصال بـ Binance
        self.exchange = ccxt.binance({
            'apiKey': API_KEY,
            'secret': SECRET,
            'enableRateLimit': True,
            'options': {'defaultType': 'spot'}
        })
        # ملاحظة: إذا أردت استخدام Testnet، فعل هذا السطر:
        # self.exchange.set_sandbox_mode(True)
        self.symbol = SYMBOL

    async def fetch_ohlcv(self, limit=100):
        """جلب بيانات الشموع (OHLCV) للبيتكوين"""
        try:
            ohlcv = await self.exchange.fetch_ohlcv(self.symbol, timeframe='1h', limit=limit)
            return ohlcv
        except Exception as e:
            logger.error(f"خطأ في جلب البيانات: {e}")
            return None

    async def close(self):
        """إغلاق الاتصال بالمنصة"""
        await self.exchange.close()

