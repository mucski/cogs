import discord
from redbot.core import commands, checks

class AdminUtils(commands.Cog):
    @commands.command()
    @checks.is_owner()
    async def addcoin(self, ctx, amt: int, member: discord.Member=None):
        if not member:
            member = ctx.author
        if not amt:
            await ctx.send("Need a value")
            return
        if amt <= 0:
            await ctx.send("Cant set bellow or equal to 0 coins")
            return
        amt += await self.conf.user(member).coins()
        await self.conf.user(member).coins.set(amt)
        await ctx.send(f"{member} now has {amt} coins")
        
    @commands.command()
    @checks.is_owner()
    async def resetcd(self, ctx):
        await self.conf.user(ctx.author).d_stamp.clear()
        await ctx.send("Cooldowns reset for 1 usage")