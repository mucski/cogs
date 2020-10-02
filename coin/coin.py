import discord
from redbot.core import commands, Config
from datetime import datetime, timedelta

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

    @coin.command()
    async def clear(self, ctx):
        self.db.clear_all()
        await ctx.send("Success!")

    @coin.command(aliases=['bal'])
    async def balance(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        async with self.db.user(member).data() as data:
            if bool(data) is False:
                await ctx.send("First claim your daily coins dummy")
                return
            try:
                coin = data['coin']
            except KeyError:
                data['coin'] = 0
                coin = data['coin']
            await ctx.send(f"Here's your dumb coin ammount: {coin}")

    @coin.command()
    async def daily(self, ctx):
        async with self.db.user(ctx.author).data() as data:
            now = datetime.utcnow()
            try:
                stamp = data['dailystamp']
                stamp = datetime.fromtimestamp(stamp)
            except KeyError:
                stamp = now
            future =  now + timedelta(hours=12)
            data['dailystamp'] = future.timestamp()
            if stamp > now:
                #await ctx.send(f"You already claimed your daily coins. Check back in {humanize.naturaldelta(stamp - now)}")
                await ctx.send(f"Come back in 12 hours")
                return
            data['coin'] += 300
            await ctx.send("Claimed 300 coins. Check back in 12 hours.")