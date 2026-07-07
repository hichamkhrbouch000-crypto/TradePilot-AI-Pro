import asyncio
from src.api.data_fetcher import DataFetcher
from src.engine.feature_engine import engine

async def test_pipeline():
    print("--- Testing Pipeline ---")
    
    # 1. جلب البيانات
    fetcher = DataFetcher(exchange_id='binance')
    df = await fetcher.fetch_ohlcv('BTC/USDT', '1h', limit=50)
    
    if not df.empty:
        print(f"Data fetched: {len(df)} candles.")
        
        # 2. تطبيق المحرك
        df_processed = engine.process(df)
        
        print("Features computed:")
        print(df_processed[['close', 'RSI', 'EMA_20']].tail())
    else:
        print("Failed to fetch data.")

if __name__ == "__main__":
    asyncio.run(test_pipeline())
