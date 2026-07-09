from config import settings
from src.trading.wallet import WalletManager
from src.trading.execution import PaperTradingEngine
import ccxt
import time
import datetime
import pandas as pd
import pandas_ta as ta
from database import log_trade, log_decision
from validator import validate_signal
from risk_manager import calculate_risk_metrics

# تهيئة المكونات باستخدام الإعدادات المركزية
wallet = WalletManager(initial_balance=settings.INITIAL_BALANCE)
paper_engine = PaperTradingEngine(wallet)

def get_market_data(exchange, symbol):
    bars = exchange.fetch_ohlcv(symbol, timeframe=settings.TIMEFRAME, limit=50)
    return pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'vol'])

def run_trading_engine():
    exchange = ccxt.kucoin()
    symbol = settings.SYMBOL
    last_checked_time = None

    print(f"--- بدء النظام المؤسسي على {symbol} ---")

    while True:
        try:
            df = get_market_data(exchange, symbol)
            current_bar_time = df['time'].iloc[-1]

            if current_bar_time != last_checked_time:
                last_checked_time = current_bar_time

                price = df['close'].iloc[-1]
                rsi = ta.rsi(df['close'], length=14).iloc[-1]

                # التحقق من الإشارات والمخاطر
                is_valid, reason = validate_signal(price, rsi)
                risk_data = calculate_risk_metrics(df, price)

                # تسجيل القرار
                decision = {
                    "timestamp": datetime.datetime.now().isoformat(),
                    "price": price,
                    "rsi": rsi,
                    "risk_decision": risk_data['is_valid'],
                    "rejection_reason": reason if not is_valid else "None",
                    "rr_ratio": risk_data.get('rr_ratio', 0)
                }
                log_decision(decision)

                # تنفيذ الصفقة بناءً على الإعدادات المركزية
                if is_valid and risk_data['is_valid']:
                    success, fee = paper_engine.execute_order(
                        symbol=symbol, 
                        side="BUY", 
                        amount=settings.POSITION_SIZE, 
                        price=price
                    )

                    if success:
                        log_trade("BUY", symbol, price)
                        print(f"تم التنفيذ بنجاح! الرسوم: {fee}")
                    else:
                        print("فشل التنفيذ: الرصيد غير كافٍ.")

            time.sleep(settings.SLEEP_INTERVAL)
            
        except Exception as e:
            print(f"خطأ في المحرك: {e}")
            time.sleep(60)

if __name__ == "__main__":
    run_trading_engine()
