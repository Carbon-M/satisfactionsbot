import sql
import discord
from discord.ext import commands, has_permissions, MissingPermissions

class AdminCommands(commands.Cog, name="Admin Commands", description="Commands for admins"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", description="Pong!")
    @has_permissions(administrator=True)
    async def ping(self, ctx):
        await ctx.send('Pong!')

    @commands.command(name="showdb", description="Show contents of the database")
    @has_permissions(administrator=True)
    async def show_db(self, ctx):
        await ctx.send("Tables:")
        await ctx.send(sql.execute_query("SHOW TABLES;"))
        await ctx.send("Factions:")
        await ctx.send(sql.execute_query("SELECT * FROM factions"))
        await ctx.send("Faction Items:")
        await ctx.send(sql.execute_query("SELECT * FROM faction_items"))
        await ctx.send("Users:")
        await ctx.send(sql.execute_query("SELECT * FROM users"))
        await ctx.send("User Invites:")
        await ctx.send(sql.execute_query("SELECT * FROM user_invites"))

    @commands.command(name="nukedb", description="Nuke the database")
    @has_permissions(administrator=True)
    async def nuke_db(self, ctx):
        sql.execute_query("DROP TABLE IF EXISTS user_invites;")
        sql.execute_query("DROP TABLE IF EXISTS users;")
        sql.execute_query("DROP TABLE IF EXISTS faction_items;")
        sql.execute_query("DROP TABLE IF EXISTS factions;")
        sql.setup_database()
        await ctx.send("Database nuked.")