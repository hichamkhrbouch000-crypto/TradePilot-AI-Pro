import ccxt
import time
import pandas as pd
import pandas_ta as ta
import logging

# --- إعداد الـ Logger ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TradePilot")

# --- محاكي المحفظة ---
class WalletManager:
    def __init__(self, initial_balance=1000):
        self.balance = initial_balance
    def get_balance(self): return self.balance

# --- محرك التنفيذ ---
class PaperTradingEngine:
    def __init__(self, wallet): self.wallet = wallet
    def execute_order(self, symbol, side, price):
        logger.info(f"تنفيذ {side} على {symbol} بسعر {price}")
        return True

# --- التحقق من الإشارة ---
def validate_signal(price, rsi):
    if rsi < 30: return True, "RSI_OVERSOLD"
    return False, "NO_SIGNAL"

# --- إدارة المخاطر ---
def calculate_risk_metrics(df, price):
    return {"is_valid": True}

# --- قاعدة البيانات ---
def log_trade(side, symbol, price):
    logger.info(f"تم تسجيل الصفقة: {side} {symbol} {price}")
def log_decision(decision):
    pass

# --- المحرك الرئيسي ---
def run_trading_engine():
    exchange = ccxt.kucoin()
    symbol = 'BTC/USDT'
    wallet = WalletManager()
    paper_engine = PaperTradingEngine(wallet)
    last_checked_time = None
    
    logger.info("--- النظام الموحد يعمل الآن ---")
    
    while True:
        try:
            bars = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=50)
            df = pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'vol'])
            current_bar_time = df['time'].iloc[-1]
            
            if current_bar_time != last_checked_time:
                last_checked_time = current_bar_time
                price = df['close'].iloc[-1]
                rsi = ta.rsi(df['close'], length=14).iloc[-1]
                
                is_valid, reason = validate_signal(price, rsi)
                if is_valid:
                    paper_engine.execute_order(symbol, "BUY", price)
                    log_trade("BUY", symbol, price)
            
            time.sleep(60)
        except Exception as e:
            logger.error(f"خطأ: {e}")
            time.sleep(300)

if __name__ == "__main__":
    run_trading_engine()
