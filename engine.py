from dataclasses import dataclass

@dataclass
class TradingConfig:
    # إعدادات عامة
    SYMBOL: str = "BTC/USDT"
    TIMEFRAME: str = "1h"
    
    # إعدادات المحفظة
    INITIAL_BALANCE: float = 20.0
    FEE_RATE: float = 0.001
    
    # إعدادات المخاطرة
    RISK_PER_TRADE: float = 0.02
    POSITION_SIZE: float = 0.0001
    
    # إعدادات النظام
    SLEEP_INTERVAL: int = 30
    
    # إعدادات أخرى
    DISCORD_WEBHOOK_URL: str = ""
    DB_PATH: str = "trading_data.db"

# كائن الإعدادات لاستخدامه في كامل المشروع
settings = TradingConfig()
