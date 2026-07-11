import ccxt
import time
import datetime
import pandas as pd
import pandas_ta as ta
import sys
import os

# إضافة المجلد الرئيسي إلى المسار لضمان عمل الـ imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# استيراد المكونات من مجلد src
from trading.wallet import WalletManager
from trading.execution import PaperTradingEngine
from engine.validator import validate_signal
from engine.risk_manager import calculate_risk_metrics
from db.database import log_trade, log_decision
from logger import get_logger

# إعداد الـ Logger
logger = get_logger("TradePilot")

def run_trading_engine():
    # إعدادات الاتصال والرموز
    exchange = ccxt.kucoin()
    symbol = 'BTC/USDT'
    timeframe = '1h'
    
    # تهيئة المحفظة والمحرك
    wallet = WalletManager(initial_balance=1000)
    paper_engine = PaperTradingEngine(wallet)
    
    last_checked_time = None 
    logger.info(f"--- النظام المؤسسي يعمل الآن على {symbol} ---")
    
    while True:
        try:
            # جلب البيانات
            bars = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=50)
            df = pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'vol'])
            
            current_bar_time = df['time'].iloc[-1]
            
            # منطق إغلاق الشمعة: يعمل فقط عند ظهور شمعة جديدة
            if current_bar_time != last_checked_time:
                last_checked_time = current_bar_time
                
                price = df['close'].iloc[-1]
                rsi = ta.rsi(df['close'], length=14).iloc[-1]
                
                # التحقق والتحليل
                is_valid, reason = validate_signal(price, rsi)
                risk_data = calculate_risk_metrics(df, price)
                
                # اتخاذ القرار
                if is_valid and risk_data['is_valid']:
                    success = paper_engine.execute_order(symbol, "BUY", price)
                    if success:
                        log_trade("BUY", symbol, price)
                        logger.info(f"تم تنفيذ صفقة شراء ناجحة بسعر {price}")
                    else:
                        logger.warning("فشل التنفيذ - رصيد غير كافٍ")
                else:
                    log_decision({"rejection_reason": reason, "price": price})
            
            time.sleep(60) # الانتظار دقيقة قبل الفحص التالي
            
        except Exception as e:
            logger.error(f"خطأ في المحرك: {str(e)}")
            time.sleep(300) # انتظار 5 دقائق في حالة حدوث خطأ قبل المحاولة مجدداً

if __name__ == "__main__":
    run_trading_engine()
