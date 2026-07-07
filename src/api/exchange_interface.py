from abc import ABC, abstractmethod

class AbstractExchangeInterface(ABC):
    """واجهة برمجية لتوحيد التعامل مع أي منصة تداول مستقبلاً"""
    
    @abstractmethod
    async def connect(self):
        """الاتصال بالمنصة"""
        pass

    @abstractmethod
    async def fetch_ohlcv(self, symbol, timeframe):
        """جلب بيانات الشموع اليابانية"""
        pass

    @abstractmethod
    async def get_balance(self, asset):
        """جلب الرصيد"""
        pass

