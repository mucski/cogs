import discord
import math
import random
import asyncio
from datetime import datetime, timedelta
from redbot.core.utils.chat_formatting import bold, box, humanize_list, humanize_number, pagify, humanize_timedelta
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
from .randomstuff import worklist
from .randomstuff import searchlist
from .randomstuff import bad_location

class Main:
    async def leaderboard(self, ctx):
        userinfo = await self.conf.all_users()
        if not userinfo:
            return await ctx.send(bold("Start playing first, then check boards."))
        sorted_acc = sorted(userinfo.items(), key=lambda x: x[1]['cookies'], reverse=True)[:50]
        li = []
        for i, (user_id, account) in enumerate(sorted_acc, start=1):
            user_obj = ctx.guild.get_member(user_id)
            if len(user_obj.display_name) < 13:
                li.append(f"#{i:2}. {user_obj.display_name:<13} {account['cookies']:>15} 🍪")
            else:
                li.append(f"#{i:2}. {user_obj.display_name[:10]:<10}... {account['cookies']:>15} 🍪")
        text = "\n".join(li)
        page_list=[]
        for page_num, page in enumerate(pagify(text, delims=['\n'], page_length=1000), start=1):
            embed=discord.Embed(
                description=box(f"Cookieboards", lang="prolog") + (box(page, lang="md")),
            )
            embed.set_footer (
                text=f"Page {page_num}/{math.ceil(len(text) / 1000)}",
            )
        page_list.append(embed)
        return await menu(ctx, page_list, DEFAULT_CONTROLS)

    async def profile(self, ctx, member):
        """ Checks your balance or some ones """
        cookie = await self.conf.user(member).cookies()
        now = datetime.utcnow().replace(microsecond=0)
        daily_stamp = await self.conf.user(member).daily_stamp()
        daily_stamp = datetime.fromtimestamp(daily_stamp)
        remaining = daily_stamp - now
        #build embed
        e = discord.Embed(timestamp=datetime.utcnow())
        e.set_author(name=f"Profile for {member.name}", icon_url=member.avatar_url)
        e.set_thumbnail(url=member.avatar_url)
        e.add_field(name="Cookies owned", value=f"``{cookie}``")
        if now < daily_stamp:
            cooling = "Yes"
            e.add_field(name="Daily on cooldown", value=f"``{cooling}``")
            e.add_field(name="Cooldown remaining", value=f"``{humanize_timedelta(timedelta=remaining)}``")
        else:
            cooling = "No"
            e.add_field(name="Daily on cooldown", value=f"``{cooling}``")
        await ctx.send(embed=e)
        
    async def work(self, ctx):
        now = datetime.utcnow().replace(microsecond=0)
        work_stamp = await self.conf.user(ctx.author).work_stamp()
        work_stamp = datetime.fromtimestamp(work_stamp)
        work_timer = timedelta(minutes=5)
        next_cd = work_timer + now
        remaining = work_stamp - now
        if now < work_stamp:
            await ctx.send(f"On cooldown. Remaining: {humanize_timedelta(timedelta=remaining)}")
            return
        """ Work to earn some cookies """
        r = random.choice(list(worklist.keys()))
        await ctx.send(worklist[r])
        def check(m):
            return m.content.lower() in r and m.guild == ctx.guild and m.author == ctx.author
        try:
            await ctx.bot.wait_for('message', timeout=7, check=check)
        except asyncio.TimeoutError:
            return await ctx.send("Have to work harder than that ...😞")
        cookie = await self.conf.user(ctx.author).cookies()
        value = random.randint(50,500)
        cookie += value
        await self.conf.user(ctx.author).cookies.set(cookie)
        await ctx.send(f"Well done, you earned ``{value}`` cookies for todays work.😴")
        await self.conf.user(ctx.author).work_stamp.set(next_cd.timestamp())
        
    async def search(self, ctx):
        r = random.sample(list(searchlist.keys()), 3)
        await ctx.send("🔍Chose a location to search from bellow🔎")
        await ctx.send(f"``{r[0]}`` , ``{r[1]}``, ``{r[2]}``")
        def check(m):
            return m.content.lower() in r and m.channel == ctx.channel and m.author == ctx.author
        try:
            msg = await ctx.bot.wait_for('message', timeout=7, check=check)
        except asyncio.TimeoutError:
            return await ctx.send("Can't search if I don't know where.")
        cookie = await self.conf.user(ctx.author).cookies()
        if msg.content.lower() in bad_location:
            return await ctx.send(searchlist[msg.content.lower()])
        else:
            amt = random.randint(50,200)
            cookie = amt + cookie
            await self.conf.user(ctx.author).cookies.set(cookie)
            return await ctx.send(searchlist[msg.content.lower()].format(amt))
    
