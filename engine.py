
from src.trading.wallet import WalletManager
from src.trading.execution import PaperTradingEngine

# تهيئة المحفظة والمحرك (نضع هذا في بداية تشغيل البوت)
wallet = WalletManager(initial_balance=20.0)
paper_engine = PaperTradingEngine(wallet)

import ccxt
import time
import datetime
import pandas as pd
import pandas_ta as ta
from database import log_trade, log_decision
from validator import validate_signal
from risk_manager import calculate_risk_metrics

def get_market_data(exchange, symbol):
    # نطلب 50 شمعة بإطار زمني 1 ساعة كما هو محدد
    bars = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=50)
    return pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'vol'])

def run_trading_engine():
    exchange = ccxt.kucoin()
    symbol = 'BTC/USDT'
    last_checked_time = None # المتغير الجديد للتحكم
    
    print("--- النظام المؤسسي: مراقبة إغلاق الشموع ---")
    
    while True:
        try:
            df = get_market_data(exchange, symbol)
            current_bar_time = df['time'].iloc[-1]
            
            # شرط جديد: لن نعمل إلا إذا كانت الشمعة قد أغلقت (وقت الشمعة تغير)
            if current_bar_time != last_checked_time:
                last_checked_time = current_bar_time
                
                price = df['close'].iloc[-1]
                rsi = ta.rsi(df['close'], length=14).iloc[-1]
                
                # ... (باقي المنطق كما هو: Validator -> Risk Manager -> Execution)
                is_valid, reason = validate_signal(price, rsi)
                risk_data = calculate_risk_metrics(df, price)
                
                # تسجيل القرار فقط عند إغلاق شمعة جديدة
                decision = {
                    "timestamp": datetime.datetime.now().isoformat(),
                    "price": price,
                    "rsi": rsi,
                    "risk_decision": risk_data['is_valid'],
                    "rejection_reason": reason if not is_valid else "None",
                    "rr_ratio": risk_data.get('rr_ratio', 0)
                }
                log_decision(decision)
                
                if is_valid and risk_data['is_valid']:
                    log_trade("BUY", symbol, price)
            
            # ننتظر 30 ثانية قبل فحص الشمعة التالية
            time.sleep(30)
        except Exception as e:
            print(f"خطأ في المحرك: {e}")
            time.sleep(60)
