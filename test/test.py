import discord
from discord import app_commands
from redbot.core import commands, checks, Config

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    slash_commands = app_commands.Group(
        name="test",
        description="Some Testing Slash Commands",
    )

    @slash_commands.command(name="test", description="List all playlists you have access to on the invoked context")
    # @app_commands.guild_only()
    async def slash_commands_test(self, interraction: discord.Interaction, user: discord.Member):
        await interaction.response.send_message(f'Hello {user}, Ya fucking cunt!...', ephemeral=True)
