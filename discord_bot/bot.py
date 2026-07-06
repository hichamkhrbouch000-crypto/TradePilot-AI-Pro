import asyncio
from discord.ext import tasks
from core.strategy import calculate_indicators, generate_signal
# ... (استيراد المكتبات الأخرى)

@tasks.loop(minutes=1) # سيحلل السوق كل دقيقة تلقائياً
async def auto_trade():
    data = exchange.fetch_ohlcv(SYMBOL, timeframe='1m', limit=100)
    indicators = calculate_indicators(data)
    signal = generate_signal(indicators)
    
    if signal == "BUY":
        # تنفيذ أمر شراء تلقائي
        exchange.create_market_buy_order(SYMBOL, amount)
        print("تم تنفيذ أمر شراء تلقائي!")
    elif signal == "SELL":
        # تنفيذ أمر بيع تلقائي
        exchange.create_market_sell_order(SYMBOL, amount)
        print("تم تنفيذ أمر بيع تلقائي!")

@bot.event
async def on_ready():
    auto_trade.start() # تشغيل المحرك التلقائي عند بدء البوت
    print("البوت جاهز ويعمل الآن في وضع التداول التلقائي!")
