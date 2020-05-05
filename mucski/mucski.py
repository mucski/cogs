import discord
import random
import asyncio
import math

from redbot.core import commands, checks, Config
from redbot.core.utils.chat_formatting import bold, box, humanize_list, humanize_number, pagify
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
from redbot.core.utils.predicates import MessagePredicate
from redbot.core.utils.embed import randomize_color

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
        r = random.choice(list(worklist.keys()))
        await ctx.send(worklist[r])
        check = MessagePredicate.lower_equal_to(r, ctx)
        try:
            msg = await ctx.bot.wait_for('message', timeout=10, check=check)
        except asyncio.TimeoutError:
            await ctx.send("Have to work harder than that ...😞")
            return
        earned = random.randint(1, 10)
        coin = await self.conf.user(ctx.author).coins()
        coin += earned
        await self.conf.user(ctx.author).coins.set(coin)
        await ctx.send(f"Well done, you earned {earned} coins for todays work.😴")
        
    @commands.command(name="leaderboard", aliases=['lb', 'cb'])
    async def leaderboard(self, ctx):
        userinfo = await self.conf.all_users()
        if not userinfo:
            await ctx.send(bold("Start playing first, then check boards."))
            return
        sorted_acc = sorted(userinfo.items(), key=lambda x: x[1]['coins'], reverse=True)[:50]
        li = []
        for i, (user_id, account) in enumerate(sorted_acc, start=1):
            user_obj = ctx.guild.get_member(user_id)
            if len(user_obj.display_name) < 13:
                li.append(f"#{i:2}. {user_obj.display_name:<13} {account['coins']:>15}")
            else:
                li.append(f"#{i:2}. {user_obj.display_name[:10]:<10}... {account['coins']:>15}")
        text = "\n".join(li)
        page_list=[]
        for page_num, page in enumerate(pagify(text, delims=['\n'], page_length=1000), start=1):
            embed=discord.Embed(
                color=await ctx.bot.get_embed_color(location=ctx.channel),
                description=box(f"Leaderboards", lang="prolog") + (box(page, lang="md")),
            )
            embed.set_footer (
                text=f"Page {page_num}/{math.ceil(len(text) / 1000)}",
            )
        page_list.append(embed)
        await menu(ctx, page_list, DEFAULT_CONTROLS) 
        