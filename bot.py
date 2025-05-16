import discord
from discord.ext import commands
import os

intents = discord.Intents.all()

TOKEN = os.getenv("TOKEN")
PREFIX = os.getenv("PREFIX", "!")  # default to "!" if not set

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

bot.load_extension("cogs.music")

bot.run(TOKEN)
