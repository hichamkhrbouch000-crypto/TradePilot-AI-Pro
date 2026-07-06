import discord
from discord.ext import commands, tasks
from config.settings import DISCORD_TOKEN, SYMBOL
from core.engine import TradingEngine
from core.strategy import calculate_indicators, generate_signal

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
engine = TradingEngine()

# كمية التداول التلقائي (مثلاً 0.001 BTC)
TRADE_AMOUNT = 0.001

@tasks.loop(minutes=1)
async def auto_trader():
    ohlcv = await engine.fetch_ohlcv(limit=100)
    if ohlcv:
        indicators = calculate_indicators(ohlcv)
        signal = generate_signal(indicators)
        
        if signal == "BUY":
            result = await engine.execute_trade("BUY", TRADE_AMOUNT)
            print(f"✅ صفقة شراء تلقائية: {result}")
        elif signal == "SELL":
            result = await engine.execute_trade("SELL", TRADE_AMOUNT)
            print(f"✅ صفقة بيع تلقائية: {result}")

@bot.event
async def on_ready():
    auto_trader.start()
    print(f"🚀 البوت يعمل الآن بوضع التداول الذكي! يراقب {SYMBOL}")

@bot.command()
async def status(ctx):
    await ctx.send("🤖 البوت يعمل في وضع التداول التلقائي ويراقب السوق.")

bot.run(DISCORD_TOKEN)
