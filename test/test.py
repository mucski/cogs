import discord
from discord import ui
from discord.ext import commands
from redbot.core import checks
from abc import ABC


class Questionnaire(ui.Modal, title='Questionnaire Response'):
    name = ui.TextInput(label='Name')
    answer = ui.TextInput(label='Answer', style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Thanks for your response, {self.name}!', ephemeral=True)


class CompositeMetaClass(type(commands.Cog), type(ABC)):
    """
    This allows the metaclass used for proper type detection to
    coexist with discord.py's metaclass
    """

    pass


class Test(commands.Cog, metaclass=CompositeMetaClass):
    def __init__(self, bot):
        self.bot = bot
        # Context menu on message
        self.react = discord.app_commands.ContextMenu(
            name="React", callback=self.react_callback
        )
        # Context menu on user
        self.user = discord.app_commands.ContextMenu(
            name="User", callback=self.user_callback
        )

    # On unload, remove the context menus and slash commands
    async def cog_unload(self):
        self.bot.tree.remove_command(self.react)
        self.bot.tree.remove_command(self.user)
        self.bot.tree.remove_command(self.slash_test)      

    # Slash command
    @commands.bot.hybrid_command(name="slash_test")
    async def slash_test(self, ctx: command.Context):
        await ctx.popupp(Questionnaire())

    # Context menu on the message 
    async def react_callback(self, interaction: discord.Interaction, message: discord.Message):
        await interaction.response.send_message('Very cool message!', ephemeral=True)

    # Context menu on the user
    async def user_callback(self, interaction: discord.Interaction, user: discord.User):
        await interaction.response.send_message('Very cool message on a user!', ephemeral=True)

    # Sync the commands
    @commands.command(name="Sync Commands", aliases=["tsc"])
    @checks.admin()
    async def sync_commands(self, ctx: commands.Context):
        self.bot.tree.add_command(self.react)
        self.bot.tree.add_command(self.user)
        self.bot.tree.add_command(self.slash_test)
        await self.bot.tree.sync()
        await ctx.tick()