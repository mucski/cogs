import discord
from redbot.core import commands, Config
from .taskhelper import TaskHelper
import asyncio


class SnapChatChan(TaskHelper, commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.load_check = self.bot.loop.create_task(self._looper())
        TaskHelper.__init__(self)
        self.conf = Config.get_conf(self, 3877191237449, force_registration=True)
        defaults = {"channel": 0}
        self.conf.register_guild(**defaults)

    @commands.command()
    async def snapchan(self, ctx, channel: discord.TextChannel):
        await self.conf.guild(ctx.guild).channel.set(channel.id)
        await ctx.send(f"Set snaptchat channel to {channel.mention}")

    @commands.command()
    async def snapstart(self, ctx):
        self.schedule_task(self._timer(15))
        await ctx.send("Snap chat started, messages will be deleted in 15 seconds.")

    async def _looper(self):
        # the loop seconds
        loop_second = 15
        await self.bot.wait_until_ready()
        guilds = await self.conf.all_guilds()
        for guild in guilds:
            guild = self.bot.get_guild(guild)
            channel = await self.conf.guild(guild).channel()
            await channel.purge(limit=1)
            self.schedule_task(self._timer(loop_second))

    async def _timer(self, loop_second):
        await asyncio.sleep(loop_second)
        await self._looper()

    @commands.command()
    async def snapstop(self, ctx):
        self.end_tasks()
        await ctx.send("Tasks should have been ended.")

    def cog_unload(self):
        self.load_check.cancel()