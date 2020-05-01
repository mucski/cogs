import discord
from redbot.core import commands, checks

class AdminUtils(commands.Cog):
    
    def shuffle(self, word):
        word = list(word)
        random.shuffle(word)
        return ''.join(word)
        
    @commands.group(name="cookie", aliases=['c'])
    @commands.guild_only()
    async def cookie(self, ctx):
        pass
     
    @cookie.command()
    @checks.is_owner()
    async def add_cookie(self, ctx, amt: int, member: discord.Member=None):
        if member is None:
            member = ctx.author
        cookie = await self.conf.user(member).cookies()
        final = cookie + amt
        await self.conf.user(member).cookies.set(final)
        await ctx.send(f"Added {amt} to {member.name} now has {cookie} cookies.")
    
    @cookie.command()
    @checks.is_owner()
    async def del_cookie(self, ctx, amt: int, member: discord.Member=None):
        if member is None:
            member = ctx.author
        cookie = await self.conf.user(member).cookies()
        final = cookie - amt
        await self.conf.user(member).cookies.set(final)
        await ctx.send(f"Removed {amt} from {membee.name} now has {cookie}")
    
    @cookie.command()
    @checks.is_owner()
    async def reset_db(self, ctx):
        await self.config.clear_all()
        await ctx.send("Thanos snapped the database.")
    
    @cookie.command()
    @checks.is_owner()
    async def reset_cd(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author
        await self.conf.user(member).daily_stamp.clear()
        await self.conf.user(member).steal_stamp.clear()
        await self.conf.user(member).work_stamp.clear()
        await ctx.send(f"All cooldowns have been reset for 1 turn for {member.name}")
        
    
