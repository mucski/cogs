import discord
import asyncio
from redbot.core.utils.predicates import MessagePredicate
from redbot.core import commands, Config
import random
import math

class Potato(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Config.get_conf(self, 8272727485, force_registration=True)
        
        default_user = {
            "data": {} #{potato: 0, and more}
        }
        default_guild = {
            "guild_data": {} #{channel: and more}
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
                silo = data['silo']
            except KeyError:
                silo = 0
            embed=discord.Embed(color=await self.bot.get_embed_color(ctx), title="🥔 potatos owned 🥔")
            embed.description=f"{ctx.author.name} has {potato} 🥔 in pocket and {silo} 🥔 stashed in silo, jelly yet?"
            await ctx.send(embed=embed)
    
    @potato.command()
    async def give(self, ctx):
        pass
    
    @potato.command()
    async def inspect(self, ctx, member: discord.Member):
        async with self.db.user(member).data() as data:
            if bool(data) is False:
                await ctx.send(f"{member.name} didn't start playing yet so no 🥔")
                return
            try:
                silo = data['silo']
            except KeyError:
                silo = 0
            e=discord.Embed(color=await self.bot.get_embed_color(ctx), title="👀 inspect 🥔")
            e.description=f"{member.name} has {data['potato']} 🥔 in their pocket and {silo} 🥔 in their silo."
            await ctx.send(embed=e)
            
    
    @potato.command()
    async def steal(self, ctx):
        pass
    
    @potato.command()
    async def farm(self, ctx):
        async with self.db.user(ctx.author).data() as data:
            pattern = (
                "```----+----+--- N ---+----+---+\n"
                " 01 | 02 | 03 | 10 | 11 | 12 \n"
                "----+----+----+----+----+---+\n"
                " 04 | 05 | 06 | 13 | 14 | 15 \n"
                "----+----+----+----+----+---+\n"
                " 07 | 08 | 09 | 16 | 17 | 18 \n"
                "W --+----+----o----+----+-- E\n"
                " 19 | 20 | 21 | 28 | 29 | 30 \n"
                "----+----+----+----+----+---+\n"
                " 22 | 23 | 24 | 31 | 32 | 33 \n"
                "----+----+----+----+----+---+\n"
                " 25 | 26 | 27 | 34 | 35 | 36 \n"
                "----+----+--- S ---+----+---+```"
            )
            potat = random.randint(1, 36)
            ne = [10,11,12,13,14,15,16,17,18]
            se = [28,29,30,31,32,33,34,35,36]
            sw = [19,20,21,22,23,24,25,26,27]
            nw = [1,2,3,4,5,6,7,8,9]
            
            if potat in ne:
                hint = "North East"
            elif potat in se:
                hint = "South East"
            elif potat in sw:
                hint = "South West"
            elif potat in nw:
                hint = "North West"
                
            e=discord.Embed(color=await self.bot.get_embed_color(ctx), title=f"{ctx.author}'s 🥔 farm")
            e.description=pattern
            e.set_footer(text=f"Your 🥔 senses are tingling, you have a feeling you should look somewhere in 🧭 {hint}")
            main = await ctx.send(embed=e)
            
            pred = MessagePredicate.same_context(ctx)
            try:
                msg = await self.bot.wait_for("message", timeout=20, check=pred)
            except asyncio.TimeoutError:
                await ctx.send("🧺 You are too slow 🧺")
                return
            try:
                resp = int(msg.content.lower())
            except ValueError:
                await ctx.send("You must input numbers.")
                return
            
            if math.isclose(resp, potat, rel_tol=0.1) is True:
                pattern = pattern.replace(str(potat), "🥔")
                e.description=pattern
                await main.edit(embed=e)
                data['potato'] = random.randint(1, 4)
                await ctx.send("Found a small 🥔, look how close you were to the big 🥔 smh..")
            elif resp == potat:
                pattern = pattern.replace(str(potat), "🥔")
                e.description=pattern
                await main.edit(embed=e)
                data['potato'] = random.randint(10, 20)
                await ctx.send("🚜 congrats you found all the 🥔")
            else:
                pattern = pattern.replace(str(potat), "🥔")
                e.description=pattern
                await main.edit(embed=e)
                await ctx.send("Found no 🥔 at all, how disappointing. You were really far.")
                return
                
    
    @potato.command()
    async def gamble(self, ctx):
        # classic roll the dice game until I figure out something better
        pass
        
    
    @potato.command()
    async def plant(self, ctx):
        async with self.db.user(ctx.author).data() as data:
            try:
                data['plant']
            except KeyError:
                data['plant'] = {}
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
                if water > 0:
                    water -= random.randint(1, 20)
                    if water < 0:
                        water = 0
                elif water == 0:
                    life -= random.randint(20, 50)
                    if life < 0:
                        e.description = (
                            f"🌞 **Life**: {0}\n"
                            f"💦 **Water**: {0}\n"
                            f"🌱 **Growth**: DEAD\n"
                            f"🧺 **Yield**: {0} 🥔"
                        )
                        await msg.edit(embed=e)
                        return
                e.description = (
                    f"🌞 **Life**: {life}\n"
                    f"💦 **Water**: {water}\n"
                    f"🌱 **Growth**:\n"
                    f"``[{growth}]``\n"
                    f"🧺 **Yield**: {0} 🥔"
                )
                await msg.edit(embed=e)
                try:
                    m = await self.bot.wait_for("message", timeout=2, check=pred)
                except asyncio.TimeoutError:
                    # code that runs when the user didn't type in anything
                    pass
                else:
                    # code that runs when the user did type in something
                    if m.content.lower() == "water":
                        water += random.randint(1, 20)
                        if water > 100:
                            water = 100
                    else:
                        pass
                    await m.delete()
                    
            if water < 50:
                amt = 2
            elif water > 50:
                amt = 4
            elif life < 90:
                amt = 1
            elif life < 50:
                amt = 0
            data['potato'] += amt
            e.description = (
                f"🌞 **Life**: {life}\n"
                f"💦 **Water**: {water}\n"
                f"🌱 **Growth**:\n"
                f"``[{growth}]``\n"
                f"🧺 **Yield**: {amt} 🥔"
            )
            await msg.edit(embed=e)
    
    @potato.command()
    async def stash(self, ctx):
        await ctx.send("How many 🥔 do you wish to stash in your silo?!")
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