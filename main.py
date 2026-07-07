import asyncio
from src.db.database import init_db
from src.api.data_fetcher import DataFetcher
from src.engine.feature_engine import engine

async def main():
    # 1. تهيئة قاعدة البيانات (تُنشئ الملف trading_bot.db تلقائياً)
    init_db()
    print("Database initialized.")
    
    # ... باقي كود الاختبار الذي كتبناه سابقاً ...

if __name__ == "__main__":
    asyncio.run(main())
