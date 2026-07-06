    async def place_order(self, side, amount):
        """تنفيذ أمر شراء أو بيع"""
        try:
            if side == "BUY":
                order = await self.exchange.create_market_buy_order(self.symbol, amount)
            else:
                order = await self.exchange.create_market_sell_order(self.symbol, amount)
            return order
        except Exception as e:
            print(f"خطأ في تنفيذ الأمر: {e}")
            return None
