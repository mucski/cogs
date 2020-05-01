import discord
import random
import math

from redbot.core import checks, commands, Config
from redbot.core.utils.chat_formatting import box, humanize_timedelta, pagify
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
from datetime import datetime, timedelta
from .adminutils import AdminUtils

class Mucski(commands.Cog):
    def __init__(self, bot):
        self.conf = Config.get_conf(self, 82838559382)
        defaults = {
            "cookies": 0,
            "daily_stamp": 0,
            "steal_stamp": 0,
            "work_stamp": 0,
        }
        self.conf.register_user(**defaults)
        
    AdminUtils(ctx)
        
    @commands.group(name="cookie", aliases=['c'])
    @commands.guild_only()
    async def cookie(self, ctx):
        pass
    
    @cookie.command()
    async def balance(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author
        cookie = await self.conf.user(member).cookies()
        await ctx.send(f"{member.name} has {cookie} cookies")
    
    @cookie.command()
    async def profile(self, ctx, member: discord.Member=None):
        pass
    
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
        pass
    
    @cookie.command()
    async def search(self, ctx):
        pass
    
    @cookie.command()
    async def scout(self, ctx):
        pass
      
    @cookie.command()
    async def daily(self, ctx):
        pass
    