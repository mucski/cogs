import asyncio
import discord
import datetime
import itertools
import math
import random
import time

from redbot.core import bank, checks, commands, Config
from redbot.core.utils.chat_formatting import bold, box, humanize_list, humanize_number, pagify
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS

class Mucski(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conf = Config.get_conf(self, 82838559382, force_registration=True)
        self.loc = {
            "cellar": "You went into the cellar looking for a fine wine, got scared by a rat and found {} cookies instead.",
            "moon": "A giant leap to man kind, Armstrong left some {} cookies here though.",
            "forest": "You went trekking into the forest, found {} cookies laying around in an abandoned camp.",
            "fridge": "Nothing beats frozen cookies, Right? Wrong. ",
            "sewer": "You descended into the sewers hoping to find a dancing clown, found {} cookies instead. ",
            "dog": "Found {} cookies in dog.... Shit. Why would you do that.. ",
            "toilet": "As disgusting as it sounds, you found {} cookies in the toilet bowl. Lucky no one used the toilet before you. ", 
            "box": "You rummaged through a box of forgotten items, found {} cookies. Lucky you. ", 
            "drawer": "After going through many panties, a dildo, and a hand gun, you found {} cookies wrapped in socks", 
            "story-book": "You were looking for Little Red Riding Hood, instead you found {} cookies hidden in a tree bark. ", 
            "set": "You are the next star for Ironing Man. While equipping his armor you found {} cookies in one of the hidden compartments. "
        }
        defaults = {
            "cookies": 0
        }
        default_guild = {
            "event_timer": 120,
            "channels": []
        }
        self.conf.register_user(**defaults)
        self.conf.register_guild(**default_guild)
    
    async def cr(self, member):
        self.conf.user(member).cookies()
    
    #test
    @commands.command()
    async def test(self, ctx, member: discord.Member):
        cookies = await self.cr(member)
        await ctx.send(f"User has {cookies} cookies")

    @commands.group(name="cookie", aliases=['c', 'ce'])
    @commands.guild_only()
    async def _cookie(self, ctx):
        """ 
        Cookie clicker game by Mucski
    
        Commands:
        `balance` - checks user balance
        `work` - earn random ammount of cookies between 100,500
        `daily` - earns 1000 cookies every 12 hours (subject to change)
        `gamble` - gambling is bad for your health
        `steal` - 60% chance of stealing someones cookie, otherwise pay them
        `lb` - leaderboards
    
        More to come.
        """
        pass
    
    @_cookie.command()
    @checks.is_owner()
    async def add(self, ctx, amount: int, *, member: discord.Member=None):
        if member is None:
            member = ctx.author
        cookie = await self.conf.user(member).cookies()
        cookie = cookie + amount
        await self.conf.user(member).cookies.set(cookie)
        await ctx.send(f"{member.name} now has {cookie} cookies.")
    
    @_cookie.command()
    @checks.is_owner()
    async def remove(self, ctx, amount: int, *, member: discord.Member=None):
        if member is None:
            member = ctx.author
        cookie = await self.conf.user(member).cookies()
        cookie = cookie - amount
        await self.conf.user(member).cookies.set(cookie)
        await ctx.send(f"{member.name} now has {cookie} cookies.")
  
    @_cookie.command()
    @checks.is_owner()
    async def clear(self, ctx):
        await self.conf.clear_all()
        await ctx.send("Database cleared.")
    
    @_cookie.command()
    async def balance(self, ctx, *, member: discord.Member=None):
        """ Checks your balance or some ones """
        if member is None:
            member = ctx.author
        cookie = await self.conf.user(member).cookies()
        await ctx.send(f"{member.name} has {cookie} cookies.")
    
    @_cookie.command()
    async def gamble(self, ctx, amount):
        """ Gamble amount of cookies with a chance to win double """
        cookie = await self.conf.user(ctx.author).cookies()
        try:
            amount = int(amount)
        except ValueError:
            if amount == 'all':
                amount = cookie
            else:
                amount = None
                await ctx.send("Can't gamble what you don't have.")
        finally:
            if amount is not None:
                if cookie - abs(amount) < 0:
                    await ctx.send("Go get yourself some cookies then try again.")
                else:
                    if random.random() < 0.3:
                        winning = amount*2
                        cookie += winning
                        await self.conf.user(ctx.author).cookies.set(cookie)
                        await ctx.send(f"Congratulations {ctx.author.name} you won {winning} cookies")
                    else:
                        cookie -= amount
                        await self.conf.user(ctx.author).cookies.set(cookie)
                        await ctx.send(f"Oops, you lost {amount} cookies.")
      
    @_cookie.command()
    async def give(self, ctx, amount, *, member: discord.Member):
        """ Give a member cookies """
        sender = await self.conf.user(ctx.author).cookies()
        try:
            amount = int(amount)
        except ValueError:
            if amount == "all":
                amount = sender
            else:
                amount = None
                await ctx.send("Thats an invalid input!")
        finally:
            if amount is not None:
                if amount >= 0:
                    if sender <= 0:
                        await ctx.send("Nope.")
                        return
                    sender -= amount
                    await self.conf.user(ctx.author).cookies.set(sender)
                    receiver = await self.conf.user(member).cookies()
                    receiver += amount
                    if receiver <= 0:
                        await ctx.send("Nope hahaha")
                        return
                    await self.conf.user(member).cookies.set(receiver)
                    await ctx.send(f"{ctx.author.name} sent {amount} cookies to {member.name}")
                else:
                    await ctx.send("Trick someone else!")
    
    @_cookie.command()
    @commands.cooldown(rate=1, per=600, type=commands.BucketType.user)
    async def work(self, ctx):
        """ Work to earn some cookies """
        value = round(random.triangular(100,500))
        cookie = await self.conf.user(ctx.author).cookies()
        cookie += value
        await self.conf.user(ctx.author).cookies.set(cookie)
        await ctx.send(f"You went to work, after a long and sweaty day you earned {value} cookies. Phew, time to relax.")
    
    @_cookie.command()
    @commands.cooldown(rate=1, per=43200, type=commands.BucketType.user)
    async def daily(self, ctx):
        """Daily cookies"""
        cookie = await self.conf.user(ctx.author).cookies()
        cookie += 1000
        await self.conf.user(ctx.author).cookies.set(cookie)
        await ctx.send(f"Claimed your daily cookies. You have {cookie} cookies now. Come back in 12 hours.")
  
    @_cookie.command()
    async def lb(self, ctx):
        """Cookieboards UwU"""
        userinfo = await self.conf.all_users()
        if not userinfo:
            return await ctx.send(bold("Start playing first, then check boards."))
        sorted_acc = sorted(userinfo.items(), key=lambda x: x[1]['cookies'], reverse=True)[:50]
        li = []
        for i, (user_id, account) in enumerate(sorted_acc, start=1):
            user_obj = ctx.guild.get_member(user_id)
            li.append(f"{i:2}. {user_obj.display_name:<15} {account['cookies']:>15}")
        text = "\n".join(li)
        page_list=[]
        for page_num, page in enumerate(pagify(text, delims=['\n'], page_length=1000), start=1):
            embed=discord.Embed(
                color=await ctx.bot.get_embed_color(location=ctx.channel),
                description=box(f"Cookieboards", lang="prolog") + (box(page, lang="md")),
            )
            embed.set_footer (
                text=f"Page {page_num}/{math.ceil(len(text) / 1000)}",
            )
        page_list.append(embed)
        return await menu(ctx, page_list, DEFAULT_CONTROLS)

    @_cookie.command()
    @commands.cooldown(rate=1, per=43200, type=commands.BucketType.user)
    async def steal(self, ctx, *, member: discord.Member=None):
        """Steal others cookies"""
        if member is None or member == ctx.author:
            await ctx.send("Really, you gonna attempt to steal from yourself?")
            return
        yourcookie = await self.conf.user(ctx.author).cookies()
        hiscookie = await self.conf.user(member).cookies()
        if yourcookie < 10000:
            await ctx.send("You're too poor to steal from others. Try again when you have at least 10000 cookies")
            return
        if hiscookie < 10000:
            await ctx.send("He or she is too poor. Can't steal from peasants. (Need at least 10000 cookies)")
            return
        value = round(random.triangular(5000,10000))
        if random.random() < 0.6:
            hiscookie -= value
            yourcookie += value
            await self.conf.user(member).cookies.set(hiscookie)
            await self.conf.user(ctx.author).cookies.set(yourcookie)
            await ctx.send(f"You've succesfully stolen {value} cookies from {member.name}.")
        else:
            hiscookie += value
            yourcookie -= value
            await self.conf.user(member).cookies.set(hiscookie)
            await self.conf.user(ctx.author).cookies.set(yourcookie)
            await ctx.send(f"You got caught! You paid {value} for apologies to {member.name}")
            
    @_cookie.command()
    async def search(self, ctx):
        """ Sesrch for cookies in random places """
        r = random.sample(list(self.loc.keys()), 3)
        await ctx.send("Chose a location to search from bellow")
        await ctx.send(f"``{r[0]}``, ``{r[1]}``, ``{r[2]}``")
        def check(m):
            return m.content.lower() in r and m.channel == ctx.channel and m.author == ctx.author
        try:
            msg = await ctx.bot.wait_for('message', timeout=10, check=check)
        except asyncio.TimeoutError:
            return await ctx.send("Can't search if I don't know where.")
        cookie = await self.conf.user(ctx.author).cookies()
        amt = int(random.triangular(100,200))
        cookie = amt + cookie
        await self.conf.user(ctx.author).cookies.set(cookie)
        return await ctx.send(self.loc[msg.content].format(amt))
    