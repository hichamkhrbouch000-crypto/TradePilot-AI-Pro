import ccxt
import time
import pandas as pd
import pandas_ta as ta
import sys
import os

# هذا السطر يضيف المجلد الرئيسي للمسار لكي يرى مجلد src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# الاستيراد الآن باستخدام المسارات الكاملة من داخل src
from src.trading.wallet import WalletManager
from src.trading.execution import PaperTradingEngine
from src.engine.validator import validate_signal
from src.engine.risk_manager import calculate_risk_metrics
from src.db.database import log_trade, log_decision
from src.logger import get_logger

logger = get_logger("TradePilot")

def run_trading_engine():
    # ... (باقي كود المحرك كما هو في الرد السابق)
    # تأكد فقط من أنك تستخدم نفس المسميات المذكورة أعلاه
