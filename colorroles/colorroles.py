import discord
from discord.utils import get
from redbot.core import commands

class ColorRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    color_roles = [
        "Black",
        "Yellow",
        "Orange",
        "Red",
        "Blue",
        "Purple",
        "Cyan",
        "Green",
    ]
    
    @commands.command()
    async def color(self, ctx, color: str):
        if color in self.color_roles:
            role = get(ctx.guild.roles, name=color)
            for role in ctx.author.roles:
                await ctx.author.remove_roles(role)
                await ctx.author.add_roles(role)
                await ctx.send("Gave role {} to {}".format(color, ctx.author))
        else:
            await ctx.send("That color is not yet available.")