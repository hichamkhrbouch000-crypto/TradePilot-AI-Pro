import discord
from discord.ext import commands
from config.settings import DISCORD_TOKEN
from core.engine import TradingEngine
from core.strategy import calculate_indicators, generate_signal

# إعداد البوت
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
engine = TradingEngine()

@bot.event
async def on_ready():
    print(f'البوت {bot.user} جاهز للعمل!')

@bot.command()
async def analyze(ctx):
    """أمر التحليل الفوري: !analyze"""
    ohlcv = await engine.fetch_ohlcv()
    if ohlcv:
        indicators = calculate_indicators(ohlcv)
        signal = generate_signal(indicators)
        
        embed = discord.Embed(title="📊 تقرير تحليل البيتكوين", color=discord.Color.gold())
        embed.add_field(name="RSI", value=f"{indicators['RSI']:.2f}", inline=True)
        embed.add_field(name="SMA20", value=f"{indicators['SMA20']:.2f}", inline=True)
        embed.add_field(name="القرار", value=f"**{signal}**", inline=False)
        
        await ctx.send(embed=embed)
    else:
        await ctx.send("❌ فشل في جلب بيانات السوق.")

# تشغيل البوت
def run_bot():
    bot.run(DISCORD_TOKEN)

