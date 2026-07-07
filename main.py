import asyncio
from engine import Engine
# سنستورد المحول (Adapter) لاحقاً عندما نربط المنصة، 
# حالياً سنقوم بتشغيل الإطار العام فقط.
from config import *

async def main():
    # هنا لاحقاً سنضع: exchange = BinanceAdapter(config)
    # حالياً نجهز الهيكل فقط.
    print("TradePilot AI Initialized.")

if __name__ == "__main__":
    asyncio.run(main())
