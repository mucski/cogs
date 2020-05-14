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
        roles = ctx.author.roles
        if color in self.color_roles:
            for color in self.color_roles:
                color = get(ctx.guild.roles, id=color)
                roles.remove(color)
                if color not in roles:
                    continue
            roles.append(color)
            await ctx.send("Success")