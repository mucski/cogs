import discord
from redbot.core import commands, Checks

class Mucski(Pet, AdminUtils, Games, Shop, commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conf = Config.get_conf(self, 28484827, force_registration=True)
        defaults = {
            "coins": 0,
            "w_stamp": 0,
            "d_stamp": 0,
            "s_stamp": 0,
            "pets": {},
        }
        self.conf.register_user(**defaults)
        
    @commands.command()
    async def balance(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.author
        amt = await self.conf.user(member).coins()
        if not amt:
            await ctx.send("User have not started playing yet")
            return
        await ctx.send(f"User has {amt} of coins")