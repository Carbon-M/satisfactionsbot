import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load .env file
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CMD_PREFIX = os.getenv('CMD_PREFIX')

# Set Intents
intents = discord.Intents.default()
intents.message_content = True

# Set Bot
bot = commands.Bot(command_prefix=CMD_PREFIX, intents=intents)

bot.run(DISCORD_TOKEN)