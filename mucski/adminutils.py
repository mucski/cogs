import random
import discord
from redbot.core import checks, commands

class AdminUtils:
    def __init__(self):
        self.bot = bot
    
    def shuffle(self, word):
        word = list(word)
        random.shuffle(word)
        return ''.join(word)
     
     
    @commands.command()    
    @checks.is_owner()
    async def add_cookie(self, ctx, member: discord.Member=None):
        pass
    
    
    @commands.command()
    @checks.is_owner()
    async def del_cookie(self, ctx, member: discord.Member=None):
        pass
    
    
    @commands.command()
    @checks.is_owner()
    async def reset_db(self, ctx):
        pass
    
    
    @commands.command()
    @checks.is_owner()
    async def reset_cd(self, ctx, member: discord.Member=None):
        pass
        
    
