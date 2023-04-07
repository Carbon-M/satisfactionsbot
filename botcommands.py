import discord
from discord.ext import commands

class BotCommands(commands.Cog, name="Bot Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')