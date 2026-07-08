import asyncio
import pandas as pd
from src.db.database import init_db
from src.api.data_fetcher import DataFetcher
from src.engine.feature_engine import engine as feature_engine
from src.strategy.engine import StrategyEngine
from src.strategy.momentum_breakout import MomentumBreakout

async def main():
    # 1. تهيئة قاعدة البيانات
    init_db()
    print("--- Database Initialized ---")

    # 2. جلب البيانات (مثال: BTC/USDT)
    fetcher = DataFetcher(exchange_id='kucoin')
    print("Fetching data...")
    df = await fetcher.fetch_ohlcv('BTC/USDT', '1h', limit=100)

    if not df.empty:
        # 3. معالجة المؤشرات
        df_processed = feature_engine.process(df)
        
        # 4. ربط وتطبيق الاستراتيجية
        strategy_engine = StrategyEngine()
        strategy_engine.set_strategy(MomentumBreakout())
        
        # اتخاذ القرار
        decision = strategy_engine.execute(df_processed)
        
        print(f"--- Strategy Decision ---")
        print(f"Signal: {decision['signal']}")
        print(f"Reason: {decision['reason']}")
    else:
        print("Error: Failed to fetch market data.")

if __name__ == "__main__":
    asyncio.run(main())
