import discord
from discord import app_commands
from redbot.core import commands


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.context_menu(name="Testing")
    async def react(interaction: discord.Interaction, message: discord.Message, user: discord.Member):
        await interaction.response.send_message(f'Hello {user}, Ya fucking cunt!...', ephemeral=True)
