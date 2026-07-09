from .wallet import WalletManager

class PaperTradingEngine:
    def __init__(self, wallet: WalletManager):
        self.wallet = wallet
        self.fee_rate = 0.001  # نسبة الرسوم (0.1%)

    def execute_order(self, symbol, side, amount, price):
        # حساب التكلفة الكلية مع الرسوم
        total_cost = amount * price
        fee = total_cost * self.fee_rate
        total_debit = total_cost + fee
        
        # محاولة حجز الأموال
        if self.wallet.reserve_funds(total_debit):
            print(f"تم تنفيذ صفقة {side} على {symbol} بسعر {price}")
            return True, fee
        else:
            print("رصيد غير كافٍ")
            return False, 0

