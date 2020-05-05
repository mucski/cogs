import discord
from redbot.core import commands, checks, Config
from redbot.core.utils.chat_formatting import bold, box, humanize_list, humanize_number, pagify, randomize_color
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
from redbot.core.utils.predicates import MessagePredicate

#self imports
from .pet import Pet
from .adminutils import AdminUtils
from .games import Games
from .shop import Shop
from .randomstuff import worklist

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
        await ctx.send(f"{member.name} has {amt} coins")
        
    @commands.command()
    async def work(self, ctx):
        r = random.choice(list(self.work.keys()))
        await ctx.send(self.work[r])
        check = MessagePredicate.lower_equal_to(r, ctx)
            msg = await ctx.bot.wait_for('message', timeout=10, check=check)
        except asyncio.TimeoutError:
            return await ctx.send("Have to work harder than that ...😞")
            earned = random.randint(1, 10)
            coin = await self.conf.user(ctx.author).coins()
            coin += earned
            await self.conf.user(ctx.author).coins.set(coin)
            await ctx.send(f"Well done, you earned ``{earned}`` cookies for todays work.😴")
        