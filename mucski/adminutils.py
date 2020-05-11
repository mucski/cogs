import discord
from redbot.core import commands, checks

class AdminUtils(commands.Cog):
    @commands.group()
    @checks.is_owner()
    async def adm(self, ctx):
        pass
    
    @adm.command()
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
        await ctx.send(f"{member.name} got {amt} now.")
        
    @adm.command()
    async def removecoin(self, ctx, amt: int, member: discord.Member=None):
        if not member:
            member = ctx.author
        if not amt:
            await ctx.send("Need a value")
            return
        coins = self.conf.user(member).coins()
        coins -= amt
        if coins < 0:
            await ctx.send("Can't go bellow 0")
            return
        await self.conf.user(member).coins.set(coins)
        await ctx.send(f"Successfully removed {amt} coins from {member.name}. {member.name} now has {coins} amount of coins.")
        
    @adm.command()
    async def resetcd(self, ctx):
        await self.conf.user(ctx.author).d_stamp.clear()
        await ctx.send("Cooldowns reset for 1 usage")
        
    @adm.command()
    async def clearall(self, ctx):
        await self.conf.clear_all()
        await ctx.send("Thanos snapped the db")
        
    @adm.command()
    async def killpet(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.author
        await self.conf.user(ctx.author).pets.clear()
        await ctx.send(f"Killed {member.name}'s pet. You bastard!")