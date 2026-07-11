import ccxt
import time
import datetime
import pandas as pd
import pandas_ta as ta
import sys
import os

# إضافة المسارات ليرى بايثون المجلدات
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from trading.wallet import WalletManager
from trading.execution import PaperTradingEngine
from engine.validator import validate_signal
from engine.risk_manager import calculate_risk_metrics
from db.database import log_trade, log_decision
from logger import get_logger

logger = get_logger("TradePilot")

def run_trading_engine():
    exchange = ccxt.kucoin()
    symbol = 'BTC/USDT'
    timeframe = '1h'
    wallet = WalletManager(initial_balance=1000)
    paper_engine = PaperTradingEngine(wallet)
    
    last_checked_time = None 
    logger.info("--- النظام يعمل الآن ---")
    
    while True:
        try:
            bars = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=50)
            df = pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'vol'])
            current_bar_time = df['time'].iloc[-1]
            
            if current_bar_time != last_checked_time:
                last_checked_time = current_bar_time
                price = df['close'].iloc[-1]
                rsi = ta.rsi(df['close'], length=14).iloc[-1]
                
                is_valid, reason = validate_signal(price, rsi)
                risk_data = calculate_risk_metrics(df, price)
                
                if is_valid and risk_data['is_valid']:
                    paper_engine.execute_order(symbol, "BUY", price)
                    log_trade("BUY", symbol, price)
                else:
                    log_decision({"rejection_reason": reason, "price": price})
            
            time.sleep(60)
        except Exception as e:
            logger.error(f"خطأ: {str(e)}")
            time.sleep(300)

if __name__ == "__main__":
    run_trading_engine()
