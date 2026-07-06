@bot.command()
async def trade(ctx):
    """أمر تنفيذ التداول التلقائي: !trade"""
    ohlcv = await engine.fetch_ohlcv()
    indicators = calculate_indicators(ohlcv)
    signal = generate_signal(indicators)
    
    if signal != "HOLD":
        # هنا يتم تنفيذ الشراء أو البيع
        order = await engine.place_order(signal, amount=0.001) # حدد الكمية هنا
        await ctx.send(f"تم تنفيذ أمر {signal} بنجاح: {order['id']}")
    else:
        await ctx.send("لا توجد إشارة تداول حالياً.")
