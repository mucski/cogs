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
        for color in self.color_roles:
            role = get(ctx.guild.roles, name=color)
            if color in roles:
                roles.remove(role)
        roles.append(role)
        await ctx.author.edit(roles=roles)
        await ctx.send("Success")