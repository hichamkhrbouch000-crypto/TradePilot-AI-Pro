from typing import Dict, Any
from .base_strategy import BaseStrategy

class StrategyEngine:
    def __init__(self):
        self.active_strategy = None
    def set_strategy(self, strategy: BaseStrategy):
        self.active_strategy = strategy
    def execute(self, df) -> Dict[str, Any]:
        if not self.active_strategy:
            raise ValueError("No strategy loaded.")
        analysis = self.active_strategy.analyze_market(df)
        signal = self.active_strategy.generate_signal(analysis)
        return {"signal": signal, "reason": analysis.get("reason", "No reason")}

