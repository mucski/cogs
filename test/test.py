from redbot.core import commands, checks, Config
import discord
from discord import app_commands

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    slash_commands = app_commands.Group(
        name="test",
        description=_("Some Testing Slash Commands"),
    )

    @slash_commands.command(name="test", description=_("List all playlists you have access to on the invoked context"))
    @app_commands.guild_only()
    async def slash_commands_test(self, interaction: InteractionT):
        await ctx.send("hello world")
