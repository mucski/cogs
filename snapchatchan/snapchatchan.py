import discord
from redbot.core import commands, Config, checks
from .taskhelper import TaskHelper
import asyncio


class SnapChatChan(TaskHelper, commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.load_check = self.bot.loop.create_task(self._looper())
        TaskHelper.__init__(self)
        self.conf = Config.get_conf(self, 3877191237449, force_registration=True)
        defaults = {"channel": 0, "timer": 0, "exclude": 0, "delete_limit": 0}
        self.conf.register_guild(**defaults)

    @commands.command()
    @checks.admin()
    async def snapchan(self, ctx, channel: discord.TextChannel):
        await self.conf.guild(ctx.guild).channel.set(channel.id)
        await ctx.send(f"Set snaptchat channel to {channel.mention}")

    @commands.command()
    @checks.admin()
    async def snaptime(self, ctx, amt: int):
        await self.conf.guild(ctx.guild).timer.set(amt)
        await ctx.send(f"Set timer to {amt} seconds.")
    
    @commands.command()
    @checks.admin()
    async def snaplimit(self, ctx, amt: int):
        await self.conf.guild(ctx.guild).delete_limit.set(amt)
        await ctx.send(f"Set timer to {amt} seconds.")

    @commands.command()
    @checks.admin()
    async def snapexclude(self, ctx, msg: int):
        await self.conf.guild(ctx.guild).exclude.set(msg)
        await ctx.send(f"The message with the id {msg} will now be excluded from deletion.")

    @commands.command()
    @checks.admin()
    async def snapstart(self, ctx):
        loop_second = await self.conf.guild(ctx.guild).timer()
        self.schedule_task(self._timer(loop_second))
        await ctx.send(f"Snap chat started, messages will be deleted in {loop_second} seconds.")

    async def _looper(self):
        await self.bot.wait_until_ready()
        guilds = await self.conf.all_guilds()
        for guild in guilds:
            # the loop seconds
            guild = self.bot.get_guild(guild)
            loop_second = await self.conf.guild(guild).timer()
            chan = await self.conf.guild(guild).channel()
            exclude = await self.conf.guild(guild).exclude()
            delete_limit = exclude = await self.conf.guild(guild).delete_limit()
            channel = self.bot.get_channel(chan)
            await channel.purge(limit=delete_limit, check=exclude)
            self.schedule_task(self._timer(loop_second))

    async def _timer(self, loop_second):
        await asyncio.sleep(loop_second)
        await self._looper()

    @commands.command()
    @checks.admin()
    async def snapstop(self, ctx):
        self.end_tasks()
        await ctx.send("Tasks should have been ended.")

    def cog_unload(self):
        self.load_check.cancel()