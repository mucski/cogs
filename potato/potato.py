import discord
import asyncio
from redbot.core.utils.predicates import MessagePredicate, ReactionPredicate
from redbot.core import commands, Config
from textwrap import dedent

class Potato(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Config.get_conf(self, 8272727485, force_registration=True)
        
        default_user = {
            "data": {} # {potato: 0, and more}
        }
        default_guild = {
            "guild_data": {} # {channel: and more}
        }
        self.db.register_user(**default_user)
        self.db.register_guild(**default_guild)
        
    @commands.group(aliases=['p'], invoke_without_command=True)
    async def potato(self, ctx):
        async with self.db.user(ctx.author).data() as data:
            if bool(data) is False:
                await ctx.send("Start playing first by using one of the action commands (farm, daily)")
                return
            potato = data['potato']
            try:
                silo = data ['silo']
            except KeyError:
                silo = 0
            embed=discord.Embed(color=await self.bot.get_embed_color(ctx), title="🥔 potatos owned 🥔")
            embed.description=f"{ctx.author.name} has {potato} 🥔 potatoes 🥔 in his pocket and {silo} 🥔 potatoes 🥔 stashed in silo, jelly yet?"
            await ctx.send(embed=embed)
    
    @potato.command()
    async def give(self, ctx):
        pass
    
    @potato.command()
    async def inspect(self, ctx):
        pass
    
    @potato.command()
    async def steal(self, ctx):
        pass
    
    @potato.command()
    async def farm(self, ctx):
        pass
    
    @potato.command()
    async def gamble(self, ctx):
        pass
    
    @potato.group(invoke_without_command=True)
    async def plant(self, ctx):
        async with self.db.user(ctx.author).data() as data:
            try:
                data['plant']
            except KeyError:
                data['plant']['life'] = 100
                data['plant']['water'] = 100
            
            life = data['plant']['life']
            water = data['plant']['water']
            e = discord.Embed(
                color=await self.bot.get_embed_color(ctx), 
                title=f"{ctx.author.name}'s 🥔 plant",
            )
            msg = await ctx.send(embed=e)
            growth = ''
            pred = MessagePredicate.same_context(ctx)
            while len(growth) < 15:
                growth += '-'
                e.description = (
                    f"🌞 **Life**: {life}\n"
                    f"💦 **Water**: {water}\n"
                    f"🌱 **Growth**:\n"
                    f"``[{growth}]``\n"
                    f"🥣 **Yield**: {0}"
                )
                await msg.edit(embed=e)
                try:
                    m = await self.bot.wait_for("message", timeout=2, check=pred)
                except asyncio.TimeoutError:
                        # code that runs when the user didn't type in anything
                    pass
                else:
                    # code that runs when the user did type in something
                    water += 10
    
    @potato.command()
    async def stash(self, ctx):
        await ctx.send("How many 🥔 potatoes 🥔 do you wish to stash in your silo?!")
        check = MessagePredicate.same_context(ctx)
        try:
            msg = await self.bot.wait_for("message", timeout=20, check=check)
        except asyncio.TimeoutError:
            await ctx.send("Need to input something, lol..")
            return
        async with self.db.user(ctx.author).data() as data:
            try:
                amount = abs(int(msg.content))
            except ValueError:
                if msg.content.lower() == "all":
                    amount = data['potato']
                else:
                    await ctx.send("Invalid input type: either a number or 'all' is required")
                    return
            if data['potato'] - amount < 0:
                await ctx.send("Not enough 🥔 to do that")
                return
            data['potato'] -= amount
            try:
                data['silo'] += amount
            except KeyError:
                data['silo'] = amount
            await ctx.send(f"Successfully stashed {amount} 🥔 in your silo.")
    
    @potato.command()
    async def daily(self, ctx):
        async with self.db.user(ctx.author).data() as data:
            data['potato'] = 1
            await ctx.send("🥔 Claimed 1 potato 🥔")