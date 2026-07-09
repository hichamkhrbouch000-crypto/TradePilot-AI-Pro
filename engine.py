import ccxt, time, datetime, pandas as pd, pandas_ta as ta, requests
from config import settings
from src.trading.wallet import WalletManager
from src.trading.execution import PaperTradingEngine
from logger import get_logger
from database import log_trade, log_decision
from validator import validate_signal
from risk_manager import calculate_risk_metrics

# تهيئة
logger = get_logger("TradePilot")
wallet = WalletManager(initial_balance=settings.INITIAL_BALANCE)
paper_engine = PaperTradingEngine(wallet)

# دالة إرسال تنبيهات ديسكورد احترافية
def send_discord_message(symbol, side, price, status):
    if not settings.DISCORD_WEBHOOK_URL: return
    data = {
        "embeds": [{
            "title": "📈 تقرير صفقة جديدة",
            "color": 65280,
            "fields": [
                {"name": "العملة", "value": symbol, "inline": True},
                {"name": "العملية", "value": side, "inline": True},
                {"name": "السعر", "value": str(price), "inline": False},
                {"name": "الحالة", "value": status, "inline": False}
            ],
            "footer": {"text": f"الوقت: {datetime.datetime.now().strftime('%H:%M:%S')}"}
        }]
    }
    try:
        requests.post(settings.DISCORD_WEBHOOK_URL, json=data)
    except Exception as e:
        logger.error(f"فشل إرسال تنبيه ديسكورد: {e}")

def run_trading_engine():
    exchange = ccxt.kucoin()
    last_trade_time = 0 # لحفظ توقيت آخر صفقة
    logger.info(f"نظام التداول بدأ على {settings.SYMBOL}")
    
    while True:
        try:
            df = exchange.fetch_ohlcv(settings.SYMBOL, timeframe=settings.TIMEFRAME, limit=50)
            df = pd.DataFrame(df, columns=['time', 'open', 'high', 'low', 'close', 'vol'])
            
            price = df['close'].iloc[-1]
            rsi = ta.rsi(df['close'], length=14).iloc[-1]
            
            # شرط التهدئة (Cooldown): لا يتداول إلا إذا مر وقت كافٍ (مثلاً 15 دقيقة = 900 ثانية)
            current_time = time.time()
            if (current_time - last_trade_time) < 900:
                time.sleep(settings.SLEEP_INTERVAL)
                continue

            is_valid, reason = validate_signal(price, rsi)
            risk_data = calculate_risk_metrics(df, price)
            
            if is_valid and risk_data['is_valid']:
                success, fee = paper_engine.execute_order(settings.SYMBOL, "BUY", settings.POSITION_SIZE, price)
                
                if success:
                    log_trade("BUY", settings.SYMBOL, price)
                    last_trade_time = current_time # تحديث توقيت آخر صفقة
                    send_discord_message(settings.SYMBOL, "BUY", price, "تم التنفيذ بنجاح")
                    logger.info(f"صفقة ناجحة: {price}")
                else:
                    send_discord_message(settings.SYMBOL, "BUY", price, "فشل التنفيذ - رصيد غير كافٍ")
            
            time.sleep(settings.SLEEP_INTERVAL)
            
        except Exception as e:
            logger.error(f"خطأ في المحرك: {str(e)}", exc_info=True)
            time.sleep(60)

if __name__ == "__main__":
    run_trading_engine()
