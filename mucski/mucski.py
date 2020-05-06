import discord
import random
import asyncio
import math
from datetime import datetime, timedelta

from redbot.core import commands, checks, Config
from redbot.core.utils.chat_formatting import bold, box, humanize_timedelta, pagify
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
from redbot.core.utils.predicates import MessagePredicate

#self imports
from .pet import Pet
from .adminutils import AdminUtils
from .games import Games
from .shop import Shop
from .randomstuff import worklist
from .randomstuff import searchlist
from .randomstuff import bad_location

class Mucski(Pet, AdminUtils, Games, Shop, commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conf = Config.get_conf(self, 28484827, force_registration=True)
        defaults = {
            "coins": 0,
            "w_stamp": 0, #work timestamp
            "d_stamp": 0, #daily timestamp
            "s_stamp": 0, #steal timestamp
            "p_stamp": 0, #pet timestamp
            "pets": {}, #pet format {hunger:100,happy:100,clean:100,type:type,mission:False,name:whatever}
        }
        self.conf.register_user(**defaults)
        
    @commands.group(name="coin", aliases=['c'], pass_context=True)
    async def coin(self, ctx):
        pass
    
    @coin.command(name="balance", aliases=['bal'])
    async def balance(self, ctx, member: discord.Member=None):
        """View the ammount of coins owned by self or someone else"""
        if not member:
            member = ctx.author
        amt = await self.conf.user(member).coins()
        if not amt:
            await ctx.send("User have not started playing yet")
            return
        await ctx.send(f"{member.name} has {amt} coins")
        
    @coin.command()
    async def work(self, ctx):
        """Work for some coins"""
        r = random.choice(list(worklist.keys()))
        await ctx.send(worklist[r])
        check = MessagePredicate.lower_equal_to(r, ctx)
        try:
            msg = await ctx.bot.wait_for('message', timeout=10, check=check)
        except asyncio.TimeoutError:
            await ctx.send("Have to work harder than that ...😞")
            return
        earned = random.randint(1, 10)
        coin = await self.conf.user(ctx.author).coins()
        coin += earned
        await self.conf.user(ctx.author).coins.set(coin)
        await ctx.send(f"Well done, you earned {earned} coins for todays work.😴")
        
    @coin.command(name="leaderboard", aliases=['lb', 'cb'])
    async def leaderboard(self, ctx):
        """View the leaderboards"""
        userinfo = await self.conf.all_users()
        if not userinfo:
            return await ctx.send(bold("Start playing first, then check boards."))
        sorted_acc = sorted(userinfo.items(), key=lambda x: x[1]['coins'], reverse=True)[:50]
        li = []
        for i, (user_id, account) in enumerate(sorted_acc, start=1):
            user_obj = ctx.guild.get_member(user_id)
            if len(user_obj.display_name) < 28:
                li.append(f"#{i:2}. {user_obj.display_name:<28} {account['coins']:>15}")
            else:
                li.append(f"#{i:2}. {user_obj.display_name[:27]:<27}... {account['coins']:>15}")
        text = "\n".join(li)
        page_list=[]
        for page_num, page in enumerate(pagify(text, delims=['\n'], page_length=1000), start=1):
            embed=discord.Embed(
                color=await ctx.bot.get_embed_color(location=ctx.channel),
                description=f"Leaderboard\n" + page,
            )
            embed.set_footer (
                text=f"Page {page_num}/{math.ceil(len(text) / 1000)}, Earn coins by claiming daily, working, and much more. Do .help Mucski to see all the available commands.",
            )
        page_list.append(embed)
        return await menu(ctx, page_list, DEFAULT_CONTROLS)
        
    @coin.command()
    async def daily(self, ctx):
        """Claim your daily coins"""
        coin = await self.conf.user(ctx.author).coins()
        #time mumbo jumbo
        now = datetime.utcnow()
        d_stamp = await self.conf.user(ctx.author).d_stamp()
        d_stamp = datetime.fromtimestamp(d_stamp)
        timer = timedelta(hours=12) #change this to desired interval
        future = timer + now
        remaining = d_stamp - now
        if d_stamp > now:
            await ctx.send(f"On cooldown for {humanize_timedelta(timedelta=remaining)}")
            return
        coin += 200
        await self.conf.user(ctx.author).coins.set(coin)
        #todo: format it properly
        await ctx.send("Claimed your daily 200 coins. Come back in 12 hours")
        #set the next daily stamp
        await self.conf.user(ctx.author).d_stamp.set(future.timestamp())
        
    @coin.command()
    async def search(self, ctx):
        """ Search for coins in random places """
        r = random.sample(list(searchlist.keys()), 3)
        await ctx.send("🔍Chose a location to search from bellow🔎\n"
                      f"``{r[0]}`` , ``{r[1]}``, ``{r[2]}``")
        check = MessagePredicate.lower_contained_in(r, ctx)
        try:
            msg = await ctx.bot.wait_for('message', timeout=7, check=check)
        except asyncio.TimeoutError:
            await ctx.send("Can't search if I don't know where.")
            return
        coin = await self.conf.user(ctx.author).coins()
        if msg.content.lower() in bad_location:
            await ctx.send(searchlist[msg.content.lower()])
            return
        else:
            amt = random.randint(1,10)
            coin += amt
            await self.conf.user(ctx.author).coins.set(coin)
            await ctx.send(searchlist[msg.content.lower()].format(amt))

    @coin.command()
    async def gamble(self, ctx, amt):
        """Classic roll the dice game 1-12"""
        coin = await self.conf.user(ctx.author).coins()
        user = random.randint(1,12)
        dealer = random.randint(1,12)
        try:
            amt = int(amt)
        except ValueError:
            if amt == 'all':
                amt = coin
        if not amt:
            await ctx.send("Need a bet amount")
            return
        if amt <= 0:
            await ctx.send("Need more coins to play.")
            return
        if amt > coin:
            await ctx.send("Not enough coins to play")
            return
        #Game logic
        if user < 12 and dealer > user:
            #you lost
            coin -= amt
            desc = (f"Dealer rolled {dealer} - You rolled {user}. You lose!")
        elif user == dealer:
            #its a tie
            desc = (f"Dealer rolled {dealer} - You rolled {user}. It is a tie.")
        elif dealer < 12 and user > dealer:
            #you won
            coin += amt
            desc = (f"Dealer rolled {dealer} - You rolled {user}. You win!")
        await self.conf.user(ctx.author).coins.set(coin)
        e = discord.Embed(description = desc)
        e.set_footer(text="You and the dealer rolls the dice. The one that has more than the other wins. You can also gamble all of your coins by typing <all> instead of a number.")
        await ctx.send(embed=e)
        
    @coin.command()
    async def steal(self, ctx, member: discord.Member):
        #TODO: Make this command interactive
        if member == ctx.author:
            await ctx.send("You gonna attempt to steal from yourself?")
        #self coin
        sc = await self.conf.user(ctx.author).coins()
        #victim coin
        vc = await self.conf.user(member).coins()
        #percentage in python is weird
        perc = random.uniform(0.05, 0.3) #you can steal 30 percent max and 5 min
        #percent is value = perc * othervalue
        #60% chance to succeed
        if random.random() < 0.6:
            vc -= round(perc * vc) #he lost
            if vc <= 0:
                await self.ctx.send("That would leave your victim broke.")
                return
            sc += round(perc * vc) #get his percentage of coins
            #finally store them
            await self.conf.user(ctx.author).coins.set(sc)
            await self.conf.user(member).coins.set(vc)
            await ctx.send(f"Success. You stolen {perc:.0%} coins from {member.name}")
        else:
            sc -= round(perc * sc) #you lost
            if sc <= 0:
                await self.ctx.send("That would leave you broke.")
                return
            vc += round(perc * sc) #get your percentage of coins
            #finally store them
            await self.conf.user(ctx.author).coins.set(sc)
            await self.conf.user(member).coins.set(vc)
            await ctx.send(f"Failed. You paid {perc:.0%} coins to {member.name} as an apology.")
            