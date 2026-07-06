import ccxt.async_support as ccxt
from config.settings import API_KEY, SECRET, SYMBOL

class TradingEngine:
    def __init__(self):
        self.exchange = ccxt.binance({
            'apiKey': API_KEY,
            'secret': SECRET,
            'enableRateLimit': True,
            'options': {'defaultType': 'spot'}
        })
        # وضع التداول التجريبي (آمن للأموال الوهمية)
        self.exchange.set_sandbox_mode(True)
        self.symbol = SYMBOL

    async def fetch_ohlcv(self, limit=100):
        try:
            return await self.exchange.fetch_ohlcv(self.symbol, timeframe='1h', limit=limit)
        except Exception:
            return None

    async def execute_trade(self, side, amount):
        try:
            if side == "BUY":
                return await self.exchange.create_market_buy_order(self.symbol, amount)
            elif side == "SELL":
                return await self.exchange.create_market_sell_order(self.symbol, amount)
        except Exception as e:
            return f"خطأ: {e}"

    async def close(self):
        await self.exchange.close()

