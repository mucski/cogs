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

    @tasks.loop(seconds=15)
    async def messager(self):
        channel = self.bot.get_channel(779860372190396447)
        await channel.purge(limit=1)

    @commands.command()
    async def task_start(self):
        the_task = self.messager.start()
        await ctx.send(f"Task started {the_task}")

    @commands.command()
    async def task_stop(self, ctx):
        the_task = self.messager.stop()
        await ctx.send(f"Task stopped {the_task}")

    @commands.command()
    async def task_running(self, ctx):
        the_task = self.messager.get_task()
        await ctx.send(the_task)