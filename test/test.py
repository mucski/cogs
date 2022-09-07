import discord
from discord import ui
from redbot.core import commands, checks
from datetime import datetime


class Questionnaire(ui.Modal, title='Questionnaire Response'):
    name = ui.TextInput(label='Name')
    answer = ui.TextInput(label='Answer', style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Thanks for your response, {self.name}!', ephemeral=True)


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.react = discord.app_commands.ContextMenu(
            name="React", callback=self.react_callback
        )
        self.user = discord.app_commands.ContextMenu(
            name="User", callback=self.user_callback
        )
        self.slash_test = discord.app_commands.CommandTree(
            name="Testing slashes", callback=self.slash_test
        )

    async def slash_test(self, interaction: discord.Interaction, message: discord.Message):
        await interaction.response.send_message("This is a slash command that is working perfectly fine.")

    async def react_callback(self, interaction: discord.Interaction, message: discord.Message):
        await interaction.response.send_message('Very cool message!', ephemeral=True)

    async def user_callback(self, interaction: discord.Interaction, user: discord.User):
        await interaction.response.send_message('Very cool message on a user!', ephemeral=True)

    @commands.command()
    @checks.admin()
    async def sync_commands(self, ctx):
        self.bot.tree.add_command(self.react)
        self.bot.tree.add_command(self.user)
        self.bot.tree.add_command(self.slash_test)
        await self.bot.tree.sync()
        await ctx.tick()

    @commands.command()
    @checks.admin()
    async def unsync_commands(self, ctx):
        self.bot.tree.remove_command(self.react)
        self.bot.tree.remove_command(self.user)
        self.bot.tree.remove_command(self.slash_test)
        await self.bot.tree.sync()
        await ctx.tick()