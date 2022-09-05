import discord
from redbot.core import commands


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.react = discord.app_commands.ContextMenu(
            name="Play on Spotify", callback=self.react
        )

    async def react(self, interaction: discord.Interaction, message: discord.Message):
        await interaction.response.send_message('Very cool message!', ephemeral=True)
        
    @commands.command()
    async def sync_commands(self, ctx):
        await self.bot.tree.sync()
        await ctx.tick()