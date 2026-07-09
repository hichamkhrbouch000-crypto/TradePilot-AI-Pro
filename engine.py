from config import settings
from src.trading.wallet import WalletManager
from src.trading.execution import PaperTradingEngine
from logger import get_logger
import ccxt, time, datetime, pandas as pd, pandas_ta as ta
from database import log_trade, log_decision
from validator import validate_signal
from risk_manager import calculate_risk_metrics

# تهيئة اللوجر
logger = get_logger("TradePilot")
wallet = WalletManager(initial_balance=settings.INITIAL_BALANCE)
paper_engine = PaperTradingEngine(wallet)

def run_trading_engine():
    exchange = ccxt.kucoin()
    logger.info(f"نظام التداول بدأ على {settings.SYMBOL}")
    
    while True:
        try:
            # استخدام مكتبة logging بدلاً من print
            df = exchange.fetch_ohlcv(settings.SYMBOL, timeframe=settings.TIMEFRAME, limit=50)
            df = pd.DataFrame(df, columns=['time', 'open', 'high', 'low', 'close', 'vol'])
            
            price = df['close'].iloc[-1]
            rsi = ta.rsi(df['close'], length=14).iloc[-1]
            
            is_valid, reason = validate_signal(price, rsi)
            risk_data = calculate_risk_metrics(df, price)
            
            if is_valid and risk_data['is_valid']:
                success, fee = paper_engine.execute_order(settings.SYMBOL, "BUY", settings.POSITION_SIZE, price)
                if success:
                    log_trade("BUY", settings.SYMBOL, price)
                    logger.info(f"صفقة ناجحة: {price} - الرسوم: {fee}")
                else:
                    logger.warning("فشل التنفيذ: رصيد غير كافٍ")
            
            time.sleep(settings.SLEEP_INTERVAL)
            
        except Exception as e:
            logger.error(f"انهيار في المحرك: {str(e)}", exc_info=True)
            time.sleep(60) # راحة عند حدوث خطأ فادح

if __name__ == "__main__":
    run_trading_engine()
