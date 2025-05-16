import discord
from discord.ext import commands
import json
import os

intents = discord.Intents.all()

with open("config.json") as f:
    config = json.load(f)

bot = commands.Bot(command_prefix=config["prefix"], intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

bot.load_extension("cogs.music")

bot.run(config["token"])
