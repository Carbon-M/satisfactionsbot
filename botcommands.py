import sql
import discord
from discord.ext import commands

class AdminCommands(commands.Cog, name="Admin Commands", description="Commands for admins"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", description="Pong!")
    @commands.has_permissions(administrator=True)
    async def ping(self, ctx):
        await ctx.send('Pong!')

    @commands.command(name="showdb", description="Show contents of the database")
    @commands.has_permissions(administrator=True)
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
    @commands.has_permissions(administrator=True)
    async def nuke_db(self, ctx):
        sql.execute_query("DROP TABLE IF EXISTS user_invites;")
        sql.execute_query("DROP TABLE IF EXISTS users;")
        sql.execute_query("DROP TABLE IF EXISTS faction_items;")
        sql.execute_query("DROP TABLE IF EXISTS factions;")
        sql.setup_database()
        await ctx.send("Database nuked.")

class FactionCommands(commands.Cog, name="Faction Commands", description="Faction related commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="createfaction", description="Create a faction")
    async def create_faction(self, ctx, name):
        author = ctx.author

        if sql.get_user_faction(author.id) != None:
            await ctx.send("You're already in a faction.")
            return
        
        if sql.get_faction_id(name) != None:
            await ctx.send("That faction already exists.")
            return
        faction_id = sql.create_faction(name)
        role = await ctx.guild.create_role(name=name)
        category = discord.utils.get(ctx.guild.categories, name="Faction Channels")

        if category is None:
            category = await ctx.guild.create_category_channel(name="Faction Channels")

        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            role: discord.PermissionOverwrite(read_messages=True)
        }
        faction_channel = await ctx.guild.create_text_channel(name, category=category, overwrites=overwrites)

        sql.set_user_faction(author.id, faction_id, True)
        sql.set_faction_item(faction_id=faction_id, channel_id=faction_channel.id, role_id=role.id)
        await author.add_roles(role)
        await ctx.send(f"Successfully created faction {name}!")

    @commands.command(name="deletefaction", description="Delete a faction")
    async def delete_faction(self, ctx):
        author = ctx.author
        faction_id = sql.get_user_faction(author.id)

        if faction_id == None:
            await ctx.send("You're not in a faction.")
            return
        
        if not sql.is_user_leader(author.id):
            await ctx.send("You're not the leader of your faction.")
            return
        faction_name = sql.get_faction_name(faction_id)
        faction_channel_id = sql.get_channel_id(faction_id)
        faction_role_id = sql.get_role_id(faction_id)

        sql.delete_faction(faction_id)
        await ctx.guild.get_channel(faction_channel_id).delete()
        await ctx.guild.get_role(faction_role_id).delete()
        await ctx.send(f"Successfully deleted faction {faction_name}!")