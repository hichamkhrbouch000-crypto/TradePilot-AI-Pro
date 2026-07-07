from .base_strategy import BaseStrategy

class MomentumBreakout(BaseStrategy):
    def analyze_market(self, df):
        last_row = df.iloc[-1]
        if last_row['close'] > last_row['EMA_20'] and last_row['RSI'] < 70:
            return {"confidence": 0.8, "reason": "Price above EMA20 and RSI healthy"}
        return {"confidence": 0, "reason": "Conditions not met"}
    def generate_signal(self, analysis):
        return "BUY" if analysis["confidence"] > 0.5 else "HOLD"

