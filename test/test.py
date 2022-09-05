import discord
from discord import app_commands
from redbot.core import commands, checks, Config


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.context_menu(discord.Member)
    async def react(interaction: discord.Interaction, message: discord.Message, user: discord.Member):
        await interaction.response.send_message(f'Hello {user}, Ya fucking cunt!...', ephemeral=True)
