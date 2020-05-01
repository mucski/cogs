import discord
import random
import math
import asyncio
from .adminutils import AdminUtils

from redbot.core import checks, commands, Config
from redbot.core.utils.chat_formatting import box, humanize_timedelta, pagify
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
from datetime import datetime, timedelta
from redbot.core.utils.predicates import MessagePredicate

#randomstuff
from .randomstuff import worklist
from .randomstuff import searchlist

class Mucski(AdminUtils, commands.Cog):
    def __init__(self, bot):
        self.conf = Config.get_conf(self, 82838559382)
        defaults = {
            "cookies": 0,
            "daily_stamp": 0,
            "steal_stamp": 0,
            "work_stamp": 0,
        }
        self.conf.register_user(**defaults)

    @commands.group(name="cookie", aliases=["c"])
    @commands.guilds_only()
    async def cookie():
        pass

    @cookie.command()
    async def balance(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author
        cookie = await self.conf.user(member).cookies()
        await ctx.send(f"{member.name} has {cookie} cookies")
    
    @cookie.command()
    async def profile(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author
        now = datetime.utcnow().replace(microsecond=0)
        cookie = await self.conf.user(member).cookies()
        daily_stamp = await self.conf.user(member).daily_stamp()
        daily_stamp = datetime.fromtimestamp(daily_stamp)
        remaining = daily_stamp - now
        e = discord.Embed(timestamp=datetime.utcnow())
        e.set_author(name=f"{member.name}'s profile", icon_url=member.avatar_url)
        e.set_thumbnail(url=member.avatar_url)
        e.add_field(name="Cookies owned", value=cookie)
        if now < daily_stamp:
            e.add_field(name="On cooldown", value="YES")
            e.add_field(name="Cooldown remaining", value=humanize_timedelta(timedelta=remaining))
        else:
            e.add_field(name="On cooldown", value="NO")
        await ctx.send(embed=e)
    
    @cookie.command(name="cookieboards", aliases=['lb', 'cb'])
    async def cookieboards(self, ctx):
        userinfo = await self.conf.all_users()
        if not userinfo:
            await ctx.send("Start playig by working, searching, scouting, or claiming your first daily.")
        sorted_acc = sorted(userinfo.items(), key = lambda x: x[1]['cookies'], reverse=True)[:50]
        text_list = []
        for i, (user_id, account) in enumerate(sorted_acc, start=1):
            user_id = ctx.guild.get_member(user_id)
            if len(user_id.name) <13:
                text_list.append(f"{i:2}, {user_id.display_name}, {account['cookies']}")
            else:
                text_list.append(f"{i:2}, {user_id.display_name}, {account['cookies']}")
        text = '\n'.join(text_list)
        page_list = []
        for page_num, page in enumerate(pagify(text, delims=["\n"], page_length=1500), start=1):
            e = discord.Embed(color = await ctx.bot.get_embed_color(location=ctx.channel), description = box(f"Cookieboards", lang="prolog") + (box(page, lang="md")))
            e.set_footer(text = f"Page {page_num}/{math.ceil(len(text) / 1500)}")
        page_list.append(e)
        return await menu(ctx, page_list, DEFAULT_CONTROLS)
    
    @cookie.command()
    async def work(self, ctx):
        work_stamp = await self.conf.user(ctx.author).work_stamp()
        work_stamp = datetime.fromtimestamp(work_stamp)
        work_timer = timedelta(minutes=5)
        now = datetime.utcnow().replace(microsecond=0)
        next_stamp = work_timer + now
        remaining = work_stamp - now
        if now < work_stamp:
            return await ctx.send(f"On cooldown. Remaining: {humanize_timedelta(timedelta=remaining)}")
        r = random.choice(list(worklist.keys()))
        await ctx.send(worklist[r])
        pred = MessagePredicate.lower_equal_to(r, ctx)
        try:
            await ctx.bot.wait_for("message", timeout=7, check=pred)
        except asyncio.TimeoutError:
            return await ctx.send("Timed out.")
        cookie = await self.conf.user(ctx.author).cookies()
        earned = random.randint(50,500)
        cookie += earned
        await self.conf.user(ctx.author).cookies.set(cookie)
        await ctx.send(f"Well done. You earned ``{earned}`` cookies for your hard work")
        await self.conf.user(ctx.author).work_stamp.set(next_stamp.timestamp())
    
    @cookie.command()
    async def search(self, ctx):
        r = random.sample(list(searchlist.keys()), 3)
        await ctx.send("Choose a location bellow")
        await ctx.send(f"{r[0]} {r[1]} {r[2]}")
        pred = MessagePredicate.contained_in(r, ctx)
        try:
            msg = await ctx.bot.wait_for("message", timeout=7, check=pred)
        except asyncio.TimeoutError:
            return await ctx.send("Timed out.")
        cookie = await self.conf.user(ctx.author).cookies()
        earned = random.randint(20,200)
        cookie += earned
        await self.conf.user(ctx.author).cookies.set(cookie)
        await ctx.send(searchlist[msg.content].format(earned))
            
    @cookie.command()
    async def scout(self, ctx):
        pass
      
    @cookie.command()
    async def daily(self, ctx):
        now = datetime.utcnow().replace(microsecond=0)
        daily_stamp = await self.conf.user(ctx.author).daily_stamp()
        daily_stamp = datetime.fromtimestamp(daily_stamp)
        daily_timer = timedelta(hours=12)
        next_stamp = daily_timer + now
        remaining = daily_stamp - now
        if now < daily_stamp:
            return await ctx.send(f"On cooldown {humanize_timedelta(timedelta=remaining)}")
        cookie = await self.conf.user(ctx.author).cookies()
        cookie += 1000
        await self.conf.user(ctx.author).cookies.set(cookie)
        await ctx.send("Claimed your daily cookies (1000)")
        await self.conf.user(ctx.author).daily_stamp.set(next_stamp.timestamp())
    