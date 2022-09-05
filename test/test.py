import discord
from redbot.core import commands


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