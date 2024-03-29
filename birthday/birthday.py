import discord
from redbot.core import commands, Config, checks
from redbot.core.utils.predicates import MessagePredicate


class Birthday(commands.Cog):
    """Birthday cog by Mucski hehehee"""
    def __init__(self, bot):
        self.bot = bot
        self.db = Config.get_conf(self, 342348495182, force_registration=True)
        default_guild = {
            "bdaychannel": "",
        }
        default_user = {
            "bdaystamp": 0,
            "dailystamp": 0,
            "stealstamp": 0,
        }


    @commands.group(aliases=['b'])
    async def birthday(self, ctx):
        """Under cumstruction"""
        pass

    @birthday.command()
    async def set(self, ctx):
        await ctx.send("Enter your birth DAY such as 03")
        bday = await self.bot.wait_for("message", check=MessagePredicate.same_context(ctx))
        try:
            bday = int(bday.content)
        except ValueError:
            await ctx.send("Must be an integer! Start over.")
            return
