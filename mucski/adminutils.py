import random
import discord
from redbot.core import checks, commands

class AdminUtils:
    
    def shuffle(self, word):
        word = list(word)
        random.shuffle(word)
        return ''.join(word)
     
     
    @cookie.command()    
    @checks.is_owner()
    async def add_cookie(self, ctx, amt: int, member: discord.Member=None):
        if member is None:
            member = ctx.author
        await self.conf.user(member).cookies.set(amt)
        await ctx.send("Added {} to {}".format(member, amt))
    
    
    @cookie.command()
    @checks.is_owner()
    async def del_cookie(self, ctx, member: discord.Member=None):
        pass
    
    
    @cookie.command()
    @checks.is_owner()
    async def reset_db(self, ctx):
        pass
    
    
    @cookie.command()
    @checks.is_owner()
    async def reset_cd(self, ctx, member: discord.Member=None):
        pass
        
    
