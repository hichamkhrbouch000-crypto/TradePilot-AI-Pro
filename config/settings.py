import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
API_KEY = os.getenv("EXCHANGE_API_KEY")
SECRET = os.getenv("EXCHANGE_SECRET")
SYMBOL = os.getenv("SYMBOL", "BTC/USDT")
