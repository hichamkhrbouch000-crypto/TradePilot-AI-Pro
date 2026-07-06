import discord
from discord.ext import commands
from config.settings import DISCORD_TOKEN
from core.engine import TradingEngine
from core.strategy import calculate_indicators, generate_signal

intents = discord.Intents.default()
intents.message_content = True # ضروري ليقرأ البوت الأوامر
bot = commands.Bot(command_prefix="!", intents=intents)
engine = TradingEngine()

@bot.command()
async def analyze(ctx):
    ohlcv = await engine.fetch_ohlcv()
    if ohlcv:
        indicators = calculate_indicators(ohlcv)
        signal = generate_signal(indicators)
        await ctx.send(f"📊 الحالة: {signal} | RSI: {indicators['RSI']:.2f}")

@bot.command()
async def buy(ctx, amount: float):
    result = await engine.execute_trade("BUY", amount)
    await ctx.send(f"✅ نتيجة أمر الشراء التجريبي: {result}")

@bot.command()
async def sell(ctx, amount: float):
    result = await engine.execute_trade("SELL", amount)
    await ctx.send(f"✅ نتيجة أمر البيع التجريبي: {result}")

def run_bot():
    bot.run(DISCORD_TOKEN)
