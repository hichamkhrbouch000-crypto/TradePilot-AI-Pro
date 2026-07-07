import ccxt.async_support as ccxt
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class DataFetcher:
    def __init__(self, exchange_id: str = 'binance'):
        self.exchange = getattr(ccxt, exchange_id)()
        
    async def fetch_ohlcv(self, symbol: str, timeframe: str, limit: int = 100) -> pd.DataFrame:
        try:
            logger.info(f"Fetching {limit} candles for {symbol}...")
            ohlcv = await self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            return df
        except Exception as e:
            logger.error(f"Error fetching data: {e}")
            return pd.DataFrame()
        finally:
            await self.exchange.close()

