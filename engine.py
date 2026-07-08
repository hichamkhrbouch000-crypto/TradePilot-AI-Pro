import ccxt
import time
import datetime
import pandas as pd
import pandas_ta as ta
from database import log_trade, log_decision
from validator import validate_signal
from risk_manager import calculate_risk_metrics

def get_market_data(exchange, symbol):
    bars = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=50)
    return pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'vol'])

def run_trading_engine():
    exchange = ccxt.kucoin()
    symbol = 'BTC/USDT'
    print("--- النظام المؤسسي بدأ العمل ---")
    
    while True:
        try:
            df = get_market_data(exchange, symbol)
            price = df['close'].iloc[-1]
            rsi = ta.rsi(df['close'], length=14).iloc[-1]
            
            # 1. طبقة التحقق
            is_valid, reason = validate_signal(price, rsi)
            
            # 2. طبقة إدارة المخاطر
            risk_data = calculate_risk_metrics(df, price)
            
            # 3. تسجيل القرار في السجل التحليلي
            decision = {
                "timestamp": datetime.datetime.now().isoformat(),
                "price": price,
                "rsi": rsi,
                "risk_decision": risk_data['is_valid'],
                "rejection_reason": reason if not is_valid else "None",
                "rr_ratio": risk_data.get('rr_ratio', 0)
            }
            log_decision(decision)
            
            # 4. التنفيذ
            if is_valid and risk_data['is_valid']:
                msg = f"✅ صفقة مقبولة: SL:{risk_data['stop_loss']:.2f} | TP:{risk_data['stop_profit']:.2f}"
                log_trade("BUY", symbol, price)
                print(msg)
            else:
                print(f"❌ الصفقة مرفوضة. السبب: {reason if not is_valid else 'Risk/Reward Low'}")
            
            time.sleep(60)
        except Exception as e:
            print(f"خطأ في المحرك: {e}")
            time.sleep(60)

if __name__ == "__main__":
    run_trading_engine()
