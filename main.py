import logging
import asyncio
from config import *

# إعداد السجلات (Logging)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

async def start_bot():
    logger.info("TradePilot AI System Starting...")
    logger.info(f"Monitoring Market: {SYMBOL} | Timeframe: {TIMEFRAME}")
    
    # هنا سيتم لاحقاً استدعاء كلاس المحرك (Engine)
    try:
        while True:
            logger.info("System heartbeat - Bot is running...")
            # هنا سنضيف المنطق التكراري لاحقاً
            await asyncio.sleep(60) 
    except Exception as e:
        logger.error(f"Critical System Failure: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")

