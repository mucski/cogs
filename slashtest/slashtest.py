import discord
from discord import app_commands
from redbot.core import commands
# from redbot.core import Config
# import asyncio


@discord.app_commands.context_menu()
async def repeat(interaction: discord.Interaction, message: discord.Message):
    await interaction.response.send_message(mesasge.content, ephemeral=True)

@discord.app_commands.context_menu()
async def hi(interraction, user: discord.Member):
    await interaction.response.send_message(f"Howdy, {user.display_name}!")


class SlashTest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #for n in range(100):
        #    c = app_commands.Command(name="flametest" + chr(n // 26 + 97) + chr(n % 26 + 97), description="desc", callback=self.callback)
        #    self.bot.tree.add_command(c)
    
    @commands.hybrid_command()
    async def flametest(self, ctx, name: str):
        """Flame is testing :P"""
        await ctx.send(f"Howdy, {name}!")
        await ctx.send(ctx.channel.permissions_for(ctx.me))
        await ctx.send(type(ctx.channel))
    
    @app_commands.command()
    async def flametesting(self, interaction, name: str):
        """Flame is testing :P"""
        await interaction.response.send_message(f"Howdy, {name}!")
    
    async def callback(self, interaction, name: str):
        """Flame is testing :P"""
        await interaction.response.send_message(f"Howdy, {name}!")
    
    @commands.command()
    async def debugstate(self, ctx):
        tree = self.bot.tree
        enabled_slash = await self.bot._config.enabled_slash_commands()
        enabled_user = await self.bot._config.enabled_user_commands()
        enabled_message = await self.bot._config.enabled_message_commands()
        
        msg = (
            f"{tree._global_commands=}\n"
            f"{tree._context_menus=}\n"
            f"{tree._disabled_global_commands=}\n"
            f"{tree._disabled_context_menus=}\n"
            f"{enabled_slash=}\n"
            f"{enabled_user=}\n"
            f"{enabled_message=}\n"
        )
        await ctx.send(f"```py\n{msg}```")
    
    async def cog_unload(self) -> None:
        self.bot.tree.remove_command("Hi", type=discord.AppCommandType.user)
        self.bot.tree.remove_command("Repeat", type=discord.AppCommandType.message)