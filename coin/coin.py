import discord
from redbot.core import commands, Config

class Coin(commands.Cog):
    """Coin Tycoon, developed by Mucski"""
    def __init__(self, bot):
        self.bot = bot
        self.db = Config.get_conf(self, 9408453854, force_registration=True)

        default_user = {
            "data": {}
        }
        default_guild = {
            "data_guild": {}
        }
        self.db.register_user(**default_user)
        self.db.register_guild(**default_guild)

    @commands.group(aliases=['c'])
    async def coin(self, ctx):
        pass

    @coin.command(aliases=['bal'])
    async def balance(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        async with self.db.user(member).data() as data:
            if bool(data) is False:
                await ctx.send("First claim your daily coins dummy")
                return
            await ctx.send(f"Here's your dumb coin ammount: {data['coin']}")

    @coin.command()
    async def daily(self, ctx):
        pass