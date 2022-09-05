import discord
from discord import app_commands
from redbot.core import commands


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.tree.command()
    async def hello(interaction: discord.Interaction):
        """Says hello!"""
        await interaction.response.send_message(f'Hi, {interaction.user.mention}')
