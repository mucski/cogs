import discord
from redbot.core import commands, Config
import random
import asyncio
from datetime import datetime, timedelta
from redbot.core.utils.chat_formatting import humanize_timedelta
from .taskhelper import TaskHelper

class Giveaway(TaskHelper, commands.Cog):
    """Simple Giveaway Cog by Mucski"""
    def __init__(self, bot):
        self.bot = bot
        self.conf = Config.get_conf(self, 975667633)
        defaults = { "channel": 0, "msg": 0, "stamp": 0, "running": False }
        self.conf.register_guild(**defaults)
        self.load_check = self.bot.loop.create_task(self._worker())
        TaskHelper.__init__(self)
    
    @commands.group(invoke_without_command=True)
    async def gw(self, ctx):
        await ctx.send("Create giveaways with ``.gw start``, stop giveaways with ``.gw stop``")
    
    @gw.command()
    async def start(self, ctx, time: int, channel: discord.TextChannel = None, *, text = None):
        if await self.conf.guild(ctx.guild).running() is True:
            await ctx.send("There is already a giveaway running.")
            return
        if channel is None:
            channel = ctx.channel
        if text is None:
            text = "Daily VIP Supreme giveaway. React bellow to enter."
        now = datetime.utcnow()
        timer = timedelta(minutes=time)
        future = timer + now
        future = future.timestamp()
        temp_stamp = datetime.fromtimestamp(future)
        remaining_timedelta = temp_stamp - now
        remaining = remaining_timedelta.total_seconds()
        #Embed Builder
        embed = discord.Embed(color = await self.bot.get_embed_color(ctx))
        embed.set_author(name=f"{self.bot.user.name}'s giveaway.", icon_url=self.bot.user.avatar_url)
        embed.description = text
        embed.set_footer(text=f"Lasts for: {humanize_timedelta(timedelta=remaining_timedelta)}")
        msg = await channel.send(embed=embed)
        await msg.add_reaction("💎")
        channel = channel.id
        msg = msg.id
        await self.conf.guild(ctx.guild).channel.set(channel)
        await self.conf.guild(ctx.guild).msg.set(msg)
        await self.conf.guild(ctx.guild).stamp.set(future)
        await self.conf.guild(ctx.guild).running.set(True)
        self.schedule_task(self._timer(remaining))
        
    @gw.command()
    async def end(self, ctx):
        msg = await self.conf.guild(ctx.guild).msg()
        if not msg:
            await ctx.send("Nothing to end")
            return
        channel = await self.conf.guild(ctx.guild).channel()
        if not channel:
            await ctx.send("Nothing to end")
            return
        await self.conf.guild(ctx.guild).stamp.clear()
        await self._worker()
        self.end_task()
        await self.conf.guild(ctx.guild).running.set(False)
        
    @gw.command()
    async def reroll(self, ctx, msgid: int, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        await self._teardown(channel, msgid, ctx.guild)
            
        
    async def _timer(self, remaining):
        await asyncio.sleep(remaining)
        await self._worker()
        
    async def _teardown(self, channel, msg, guild):
        if await self.conf.guild(guild).running() is False:
            return
        channel = self.bot.get_channel(channel)
        msg = await channel.fetch_message(msg)
        users = []
        async for user in msg.reactions[0].users():
            if user == self.bot.user:
                continue
            users.append(user)
        #await self.conf.guild(guild).msg.clear()
        #await self.conf.guild(guild).channel.clear()
        #await self.conf.guild(guild).stamp.clear()
        await self.conf.guild(guild).running.set(False)
        #Embed Builder
        embed = discord.Embed(color = await self.bot.get_embed_color(location = channel))
        embed.set_author(name=f"{self.bot.user.name}'s giveaway.", icon_url=self.bot.user.avatar_url)
        embed.description = "Giveaway finished. See bellow for winners:"
        embed.set_footer(text=f"Giveaway finished.")
        await msg.edit(embed=embed)
        if users:
            winner = random.choice(users)
            await channel.send(f"The winner is {winner.mention}, congratulations! 🎉🎊")
        else:
            await channel.send(f"No one even tried, how sad is that.")
        
    async def _worker(self):
        await self.bot.wait_until_ready()
        guilds = await self.conf.all_guilds()
        for guild in guilds:
            guild = self.bot.get_guild(guild)
            now = datetime.utcnow()
            stamp = await self.conf.guild(guild).stamp()
            stamp = datetime.fromtimestamp(stamp)
            remaining_timedelta = stamp - now
            remaining = remaining_timedelta.total_seconds()
            msg = await self.conf.guild(guild).msg()
            channel = await self.conf.guild(guild).channel()
            if stamp < now:
                await self._teardown(channel, msg, guild)
            else:
                self.schedule_task(self._timer(remaining))
    
    def cog_unload(self):
        self.load_check.cancel()