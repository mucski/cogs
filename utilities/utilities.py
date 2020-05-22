import discord
from redbot.core import commands

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(aliases = ["emoji"])
    async def emote(self, ctx, emoji: discord.PartialEmoji):
        await ctx.send(emoji.url)
        
    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        await ctx.send(member.avatar_url)