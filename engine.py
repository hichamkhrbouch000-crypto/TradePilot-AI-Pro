import ccxt
import time
import pandas as pd
import pandas_ta as ta
from database import log_trade
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
            
            if is_valid:
                # 2. طبقة إدارة المخاطر (المدير المالي)
                risk_data = calculate_risk_metrics(df, price)
                
                if risk_data['is_valid']:
                    # 3. التنفيذ (إذا وافق المدير المالي)
                    msg = f"✅ صفقة مقبولة: SL:{risk_data['stop_loss']:.2f} | TP:{risk_data['take_profit']:.2f} | RR:{risk_data['rr_ratio']:.2f}"
                    log_trade("BUY", symbol, price)
                    print(msg)
                else:
                    print(f"❌ المدير المالي رفض الصفقة: RR منخفض ({risk_data['rr_ratio']:.2f})")
            else:
                print(f"⚠️ الإشارة مرفوضة من الفلتر: {reason}")
            
            time.sleep(60)
        except Exception as e:
            print(f"خطأ في المحرك: {e}")
            time.sleep(60)

if __name__ == "__main__":
    run_trading_engine()
