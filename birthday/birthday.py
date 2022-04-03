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
        await ctx.send("Enter your birth DAY")
        bday = await self.bot.wait_for("message", check=MessagePredicate.same_context(ctx))
        if len(bday.content) < 2 or len(bday.content) > 2:
            await ctx.send("Birth day must be a two digit number (01 ... and so on), run the command again to start over")
            return
        await ctx.send("Enter your birth MONTH")
        bmonth = await self.bot.wait_for("message", check=MessagePredicate.same_context(ctx))
        if len(bmonth.content) < 2 or len(bmonth.content) > 2:
            await ctx.send("Birth month must be a two digit number (01 ... and so on), run the command again to start over")
            return
        elif not isinstance(bmonth.content, int):
            await ctx.send("You must enter a 2 digit number")
            return
        await ctx.send("Enter your birth YEAR")
        byear = await self.bot.wait_for("message", check=MessagePredicate.same_context(ctx))
        if len(byear.content) < 4 or len(byear.content) > 4:
            await ctx.send("Birth year must be a four digit number (01 ... and so on), run the command again to start over")
            return
        await ctx.send("You set your birthday to {}/{}/{}".format(bday.content,bmonth.content,byear.content))
