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
        "Hot Pink",
        "Pink",
        "Green",
    ]
    
    @commands.command()
    async def color(self, ctx, *, color: str):
        if color in self.color_roles:
            roles = ctx.author.roles
            for colors in self.color_roles:
                try:
                    roles.remove(colors)
                except ValueError
                except ValueError
                    roles.append(color)
            await ctx.author.edit(roles=roles)
            await ctx.send("Gave {} to {}".format(color, ctx.author))