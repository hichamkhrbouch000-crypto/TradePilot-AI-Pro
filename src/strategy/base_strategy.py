from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseStrategy(ABC):
    @abstractmethod
    def analyze_market(self, df: Any) -> Dict[str, Any]:
        """تحليل البيانات وإرجاع إشارة وقرار."""
        pass

    @abstractmethod
    def generate_signal(self, analysis: Dict[str, Any]) -> str:
        """توليد الإشارة (BUY/SELL/HOLD)."""
        pass

