from redbot.core import commands, Config
import random
from redbot.core.utils.menus import start_adding_reactions
from redbot.core.utils.predicates import ReactionPredicate
from discord.ext import tasks


class Test(commands.Cog):
    def __init__(self, bot):
        self.conf = Config.get_conf(self, 9340293423)
        defaults = {
            "msgs": {}
        }
        self.conf.register_guild(**defaults)
        self.bot = bot

    @commands.command()
    async def msglaunch(self, ctx):
        msg = await self.conf.guild(ctx.guild).msgs.get_raw()
        await ctx.send(msg)

    @commands.command()
    async def msgdefine(self, ctx, msg1, msg2):
        await self.conf.guild(ctx.guild).msgs.set_raw(value=+{msg1: msg2})
        await ctx.send("Done")

    @tasks.loop(seconds=15, reconnect=False)
    async def messager(self):
        channel = self.bot.get_channel(779860372190396447)
        await channel.purge(limit=1)

    @commands.command()
    async def task_start(self, ctx):
        self.messager.start()
        await ctx.send("Task started")

    @commands.command()
    async def task_stop(self, ctx):
        self.messager.stop()
        await ctx.send("Task stopped")

    @commands.command()
    async def task_cancel(self, ctx):
        self.messager.cancel()
        await ctx.send("Task cancelled")

    @commands.command()
    async def task_running(self, ctx):
        the_task = self.messager.get_task()
        if the_task is None:
            the_task = "No task to display"
        await ctx.send(the_task)