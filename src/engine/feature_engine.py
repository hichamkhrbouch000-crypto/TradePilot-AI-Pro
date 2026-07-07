import pandas as pd
import pandas_ta as ta
import logging
from typing import List, Callable

logger = logging.getLogger(__name__)

class FeatureEngine:
    """محرك الميزات: يقوم بإثراء بيانات OHLCV بالمؤشرات الفنية."""
    def __init__(self):
        self._indicators: List[Callable[[pd.DataFrame], pd.DataFrame]] = []

    def register_indicator(self, indicator_func: Callable[[pd.DataFrame], pd.DataFrame]):
        """تسجيل مؤشر جديد للعملية."""
        self._indicators.append(indicator_func)
        return indicator_func

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        """تطبيق جميع المؤشرات المسجلة على DataFrame."""
        df_enriched = df.copy()
        for indicator in self._indicators:
            try:
                df_enriched = indicator(df_enriched)
            except Exception as e:
                logger.error(f"Error applying indicator: {e}")
        return df_enriched.dropna()

# تهيئة المحرك
engine = FeatureEngine()

# أمثلة للمؤشرات (يمكنك إضافة المزيد لاحقاً)
@engine.register_indicator
def add_common_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df['RSI'] = ta.rsi(df['close'], length=14)
    df['EMA_20'] = ta.ema(df['close'], length=20)
    return df

