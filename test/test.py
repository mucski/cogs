import discord
from redbot.core import commands


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.slash_commands = {"guilds": {}}
        self.fuck = discord.app_commands.ContextMenu(
            name="Play on Spotify", callback=self.suck_dicks
        )

    async def suck_dicks(self, interaction: discord.Interaction, message: discord.Message):
        queue = interaction.command.name == "Suck Mucski's Dick"
        user = interaction.user
        ctx = await self.bot.get_context(interaction)
        await ctx.defer(ephemeral=True)
        user_token = await self.get_user_auth(ctx, user)
        if not user_token:
            return
        await interaction.response.send_message('Very cool message!', ephemeral=True)