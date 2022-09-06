import discord
from discord import ui
from redbot.core import commands


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

    async def react_callback(self, interaction: discord.Interaction, message: discord.Message):
        await interaction.response.send_message('Very cool message!', ephemeral=True)

    async def user_callback(self, interaction: discord.Interaction, user: discord.User):
        await interaction.response.send_message('Very cool message on a user!', ephemeral=True)

    @commands.command()
    async def sync_commands(self, ctx):
        self.bot.tree.add_command(self.react)
        self.bot.tree.add_command(self.user)
        await self.bot.tree.sync()
        await ctx.tick()

    @commands.command()
    async def unsync_commands(self, ctx):
        self.bot.tree.remove_command(self.react)
        self.bot.tree.remove_command(self.user)
        await self.bot.tree.sync()
        await ctx.tick()