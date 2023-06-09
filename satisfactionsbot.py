import os
import sql
import asyncio
import discord
import botcommands
from discord.ext import commands
from dotenv import load_dotenv

# Load .env file
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CMD_PREFIX = os.getenv('CMD_PREFIX')

# Setup Database
sql.setup_database()

# Set Intents
intents = discord.Intents.default()
intents.message_content = True

# Set Bot
bot = commands.Bot(command_prefix=CMD_PREFIX, intents=intents)

# Load Cogs
async def add_cogs():
    await bot.add_cog(botcommands.AdminCommands(bot))
    await bot.add_cog(botcommands.FactionCommands(bot))

asyncio.run(add_cogs())

bot.run(DISCORD_TOKEN)