class WalletManager:
    def __init__(self, initial_balance=20.0):
        self.available_balance = initial_balance
        self.reserved_balance = 0.0
        self.total_equity = initial_balance

    def reserve_funds(self, amount):
        if amount > self.available_balance:
            return False
        self.available_balance -= amount
        self.reserved_balance += amount
        return True

    def release_funds(self, amount, pnl):
        self.reserved_balance -= amount
        self.available_balance += (amount + pnl)
        self.total_equity = self.available_balance + self.reserved_balance

    def get_status(self):
        return {
            "available": self.available_balance,
            "reserved": self.reserved_balance,
            "total": self.total_equity
        }

