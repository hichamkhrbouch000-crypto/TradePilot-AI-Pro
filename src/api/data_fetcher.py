import os
import ccxt

api_key = os.getenv('EXCHANGE_API_KEY')
api_secret = os.getenv('EXCHANGE_SECRET')

# ثم استخدمهما عند تهيئة المنصة
exchange = ccxt.kucoin({
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit': True,
    'options': {'sandboxMode': True} # ستفعل هذا غداً
})
