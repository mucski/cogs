import discord
import random
from datetime import datetime, timedelta
from redbot.core import commands, checks
from .adminutils import AdminUtils
from redbot.core.utils.chat_formatting import humanize_timedelta


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
            await ctx.send(f"FCI gonna be looking for you. Try again in {humanize_timedelta(timedelta=remaining)}")
            return
        if member is None or member == ctx.author:
            await ctx.send("Really, you gonna attempt to steal from yourself?")
            return
        you = await self.conf.user(ctx.author).cookies()
        victim = await self.conf.user(member).cookies()
        if you < 0:
            msg = "That would be yer last cookie mate. Can't allow that now can I."
            return
        if victim < 0:
            msg = "Taking other peoples last cookie .. really?."
            return
        percent = random.uniform(0.05,0.3)
        if random.random() < 0.6:
            victim -= round(percent * victim)
            if victim <= 0:
                msg = "Yeah ... no. Not worth it."
                return
            you += round(percent * victim)
            await self.conf.user(member).cookies.set(victim)
            await self.conf.user(ctx.author).cookies.set(you)
            msg = f"💎 You've succesfully stolen ``{percent:.0%}`` cookies from ``{member.name}``. 😱"
        else:
            victim += round(percent * you)
            you -= round(percent * you)
            if you <= 0:
                msg = "Yeah, you can't go negative, buster."
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
                error = "It's called gambling, not UNICEF"
        finally:
            if amount is not None:
                if amount <= 0:
                    error = "You hit rock bottom. Can't go any further."
                elif cookie - amount < 0:
                    error = "Need some cookies? Then go get yourself some, and stop bugging me."
                else:
                    #Game logic
                    e = discord.Embed(timestamp=datetime.utcnow())
                    e.set_author(name=f"{ctx.author.name} rolls the cookie.", icon_url=ctx.author.avatar_url)
                    e.set_thumbnail(url=ctx.bot.user.avatar_url)
                    if member < 6 and dealer > member:
                        msg = f"Haha! Got ya! You lost ``{amount}`` cookies. 😞"
                        cookie -= amount
                        await self.conf.user(ctx.author).cookies.set(cookie)
                    elif member == dealer:
                        msg = f"What a pitty, looks like its a tie."
                    elif dealer < 6 and dealer < member:
                        msg = f"{ctx.bot.user.name} got rekt. You won ``{amount}`` cookies. 😱"
                        cookie += amount
                        await self.conf.user(ctx.author).cookies.set(cookie)
                    e.description = msg
                    e.add_field(name=f"{ctx.bot.user.name} rolled", value=f"🍪 {dealer}")
                    e.add_field(name="You rolled", value=f"🍪 {member}")
        try:
            if error is None:
        except UnboundLocalError:
                await ctx.send(embed=e)
            else:
                await ctx.send(error)
            
