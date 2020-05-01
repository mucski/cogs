import discord
import random
from datetime import datetime, timedelta
from redbot.core import commands, checks
from .adminutils import AdminUtils

class Games(commands.Cog):
    
    @AdminUtils.cookie.command()
    async def steal(self, ctx, member: discord.Member):
        now = datetime.utcnow().replace(microsecond=0)
        steal_stamp = await self.conf.user(ctx.author).steal_stamp()
        steal_stamp = datetime.fromtimestamp(steal_stamp)
        steal_timer = timedelta(hours=6)
        next_cd = steal_timer + now
        remaining = steal_stamp - now
        if now < steal_stamp:
            await ctx.send(f"On cooldown. Remaining: {humanize_timedelta(timedelta=remaining)}")
            return
        if member is None or member == ctx.author:
            await ctx.send("Really, you gonna attempt to steal from yourself?")
            return
        you = await self.conf.user(ctx.author).cookies()
        victim = await self.conf.user(member).cookies()
        if you < 0:
            msg = "You're too poor to steal from others."
            return
        if victim < 0:
            msg = "He or she is too poor. Can't steal from peasants."
            return
        percent = random.uniform(0.05,0.3)
        if random.random() < 0.6:
            victim -= round(percent * victim)
            if victim <= 0:
                msg = "User doesn't have enough cookies."
                return
            you += round(percent * victim)
            await self.conf.user(member).cookies.set(victim)
            await self.conf.user(ctx.author).cookies.set(you)
            msg = f"💎 You've succesfully stolen ``{percent:.0%}`` cookies from ``{member.name}``. 😱"
        else:
            victim += round(percent * you)
            you -= round(percent * you)
            if you <= 0:
                msg = "You dont have enough cookies."
                return
            await self.conf.user(member).cookies.set(victim)
            await self.conf.user(ctx.author).cookies.set(you)
            msg = f"👮‍♂️ You got caught! You paid ``{percent:.0%}`` of your cookies for apologies to ``{member.name}`` 😭"
        await ctx.send(msg)
        await self.conf.user(ctx.author).steal_stamp.set(next_cd.timestamp())
            
    
    @AdminUtils.cookie.command()
    async def gamble(self, ctx, amount):
        member = random.randint(1,6)
        dealer = random.randint(1,6)
        cookie = await self.conf.user(ctx.author).cookies()
        try:
            amount = int(amount)
        except ValueError:
            if amount == 'all':
                amount = cookie
            else:
                amount = None
                msg = "Need more cookies to play."
        finally:
            if amount is not None:
                if amount <= 0:
                    msg = "Invalid amount of cookies!"
                elif cookie - amount < 0:
                    msg = "Get yourself some cookies first"
                else:
                    #Game logic
                    e = discord.Embed(timestamp=datetime.utcnow())
                    e.set_author(name=f"{ctx.author.name} rolls the dice.", icon_url=ctx.author.avatar_url)
                    e.set_thumbnail(url=ctx.bot.user.avatar_url)
                    if member < 6 and dealer > member:
                        msg = f"Busted. You lost ``{amount}`` cookies. 😞"
                        cookie -= amount
                        await self.conf.user(ctx.author).cookies.set(cookie)
                    elif member == dealer:
                        msg = f"Looks like its a tie."
                    elif dealer < 6 and dealer < member:
                        msg = f"{ctx.bot.user.name} busted. You won ``{amount}`` cookies. 😱"
                        cookie += amount
                        await self.conf.user(ctx.author).cookies.set(cookie)
                    e.description = msg
                    e.add_field(name="Dealer rolled", value=f"🍪 {dealer}")
                    e.add_field(name="You rolled", value=f"🍪 {member}")
        if e is None:
            await ctx.send(msg)
        else:
            await ctx.send(embed=e)
            
