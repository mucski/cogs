import asyncio
import discord
from datetime import datetime, timedelta
import itertools
import math
import random
import time

from redbot.core import bank, checks, commands, Config
from redbot.core.utils.chat_formatting import bold, box, humanize_list, humanize_number, pagify, humanize_timedelta
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS

class Mucski(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conf = Config.get_conf(self, 82838559382, force_registration=True)
        self.loc = {
            "cellar": "You went into the cellar looking for a fine wine, got scared by a rat and found ``{}`` cookies instead.",
            "moon": "A giant leap to man kind, Armstrong left some ``{}`` cookies here though.",
            "forest": "You went trekking into the forest, found ``{}`` cookies laying around in an abandoned camp.",
            "fridge": "Nothing beats frozen cookies, Right? Wrong.",
            "sewer": "You descended into the sewers hoping to find a dancing clown, found ``{}`` cookies instead. ",
            "dog": "Why would you do that.. that's animal abuse.",
            "toilet": "Why would you search a toilet... That's disgusting and so are you. ", 
            "box": "You rummaged through a box of forgotten items, found ``{}`` cookies. Lucky you. ", 
            "drawer": "After going through many panties, a dildo, and a hand gun, you found ``{}`` cookies wrapped in socks", 
            "story book": "You were looking for Little Red Riding Hood, instead you found ``{}`` cookies hidden in a tree bark. ", 
            "set": "You are the next star for Ironing Man. While equipping his armor you found ``{}`` cookies in one of the hidden compartments. ",
            "hospital": "You searched the hospital and found ``{}`` cookies. Don't eat them though, may be infected with covid19.",
            "school": "You went looking for cookies in your school locker, got a wedgy out of it instead. Bullies.",
            "trash": "Found nothing. Must've picked the wrong trash.",
        }
        self.badloc = ['fridge','dog','toilet','trash','school']
        self.work = {
            "hot dog":"You are working outside with a cart. Un scramble the following word ``dot goh``", 
            "cauterize": "You're a pro Paladins player. What do you buy first at match start? ", 
            "covid19": "You can't work cause of Quarantine. Kill the virus ``c _ _ _ _ _ _``",
            "jack sparrow": "You're a famous Pirate. Who are you?", 
            "bulbbulb": "Type the following word in reverse ``blubblub``", 
            "dick": "You are working as a professional hunter. Shot the u out of a duck.",
            "redbot": "I'm a bot, but do you know my name?",
            "mucski": f"Had to include it here ... Unscramble me. ``{self.shuffle_word('mucski')}``",
            "paladins": f"Unscramble the following word ``{self.shuffle_word('paladins')}``",
            "depression": f"Unscramble the following word ``{self.shuffle_word('depression')}``",
        }
        defaults = {
            "cookies": 0,
            "daily_stamp": 0,
            "steal_stamp": 0,
            "work_stamp": 0,
        }
        default_guild = {
            "event_timer": 120,
            "daily_timer": 0, #hours
            "steal_timer": 0, #hours
            "work_timer": 0, #minutes
            "channels": []
        }
        self.conf.register_user(**defaults)
        self.conf.register_guild(**default_guild)
    
    #View cookies
    async def cv(self, member):
        return await self.conf.user(member).cookies()
    
    #Add or remove cookies
    async def cd(self, member, amt):
        return await self.conf.user(member).cookies.set(amt)
        
    #Shuffle only works on lists, so converting word to list then word
    def shuffle_word(self, word):
        word = list(word)
        random.shuffle(word)
        return ''.join(word)
    
    #Get thet bot color for embeds 'await self.color(ctx)'
    async def color(self, ctx):
        return await ctx.bot.get_embed_color(location=ctx.channel)
    
    #test
    @commands.command()
    async def bal(self, ctx):
        color = await self.color(ctx)
        await ctx.send(color)

    @commands.group(name="cookie", aliases=['c', 'ce'])
    @commands.guild_only()
    async def _cookie(self, ctx):
        """ 
        Cookie clicker game by Mucski
    
        Commands:
        `search` - search for cookies in random locations
        `profile` - view your stats and profile
        `work` - earn random ammount of cookies
        `daily` - earns 1000 cookies every 12 hours (subject to change)
        `gamble` - gambling is bad for your health
        `steal` - steal someones cookies
        `leaderboard or lb` - leaderboards
        `roll` - another form of gambling (roll the dice)
    
        More to come.
        """
        pass
    
    @_cookie.command()
    @checks.is_owner()
    async def add(self, ctx, amount: int, *, member: discord.Member=None):
        """ Only shown to owner, adds cookies to test"""
        if member is None:
            member = ctx.author
        cookie = await self.cv(member)
        cookie = cookie + amount
        await self.cd(member,cookie)
        await ctx.send(f"``{member.name}`` now has ``{cookie}`` cookies.")
    
    @_cookie.command()
    @checks.is_owner()
    async def remove(self, ctx, amount: int, *, member: discord.Member=None):
        """Test cookie removal"""
        if member is None:
            member = ctx.author
        cookie = await self.cv(member)
        cookie = cookie - amount
        await self.cd(member,cookie)
        await ctx.send(f"``{member.name}`` now has ``{cookie}`` cookies.")
  
    @_cookie.command()
    @checks.is_owner()
    async def clear(self, ctx):
        """Clears the entire db"""
        await self.conf.clear_all()
        await ctx.send("Database cleared.")
    
    @_cookie.command(name="profile", aliases=['balance'])
    async def profile(self, ctx, *, member: discord.Member=None):
        """ Checks your balance or some ones """
        if member is None:
            member = ctx.author
        cookie = await self.cv(member)
        now = datetime.utcnow().replace(microsecond=0)
        daily_stamp = await self.conf.user(member).daily_stamp()
        if now.timestamp() < daily_stamp:
            cooling = "Yes"
        else:
            cooling = "No"
        #build embed
        e = discord.Embed(color=await self.color(ctx))
        e.set_author(name=f"Profile for {member.name}", icon_url=member.avatar_url)
        e.set_thumbnail(url=member.avatar_url)
        e.add_field(name="Cookies owned", value=f"``{cookie}``")
        e.add_field(name="Daily on cooldown", value=f"``{cooling}``")
        e.add_field(name="Cooldown until", value=f"``{datetime.fromtimestamp(daily_stamp)}``")
        e.set_footer(text=datetime.utcnow())
        await ctx.send(embed=e)
        
    @_cookie.command()
    async def gamble(self, ctx, amount):
        """Roll the dice see if you win"""
        member = random.randint(1,6)
        dealer = random.randint(1,6)
        cookie = await self.cv(ctx.author)
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
                    if member < 6 and dealer > member:
                        msg = f"Busted. You lost ``{amount}`` cookies."
                        cookie -= amount
                        await self.cd(ctx.author,cookie)
                    elif member == dealer:
                        msg = f"Looks like its a tie."
                    elif dealer < 6 and dealer < member:
                        msg = f"Dealer busted. You won ``{amount}`` cookies."
                        cookie += amount
                        await self.cd(ctx.author,cookie)
        embed = discord.Embed(color=await self.color(ctx), description=f"{msg}")
        embed.set_author(name=f"{ctx.author.name} rolls the dice.", icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=ctx.bot.user.avatar_url)
        embed.add_field(name="Dealer rolled", value=f"🎲 {dealer}")
        embed.add_field(name="You rolled", value=f"🎲 {member}")
        embed.set_footer(text=datetime.datetime.utcnow())
        await ctx.send(embed=embed)
            
    @_cookie.command()
    async def give(self, ctx, amount, *, member: discord.Member):
        """ Give a member cookies """
        sender = await self.cv(ctx.author)
        try:
            amount = int(amount)
        except ValueError:
            if amount == "all":
                amount = sender
            else:
                amount = None
                msg = "Thats an invalid input!"
        finally:
            if amount is not None:
                if amount >= 0:
                    if sender <= 0:
                        msg = "Nope."
                        return
                    sender -= amount
                    await self.cd(ctx.author,sender)
                    receiver = await self.cv(member)
                    receiver += amount
                    if receiver <= 0:
                        msg = "Nope hahaha"
                        return
                    await self.cd(member,receiver)
                    msg = f"``{ctx.author.name}`` sent ``{amount}`` cookies to ``{member.name}`` 🍪🎉"
                else:
                    msg = "Trick someone else!"
        await ctx.send(msg)
    
    @_cookie.command()
    async def work(self, ctx):
        member = ctx.author
        now = datetime.utcnow().replace(microsecond=0)
        work_stamp = await self.conf.user(member).work_stamp()
        timer = await self.conf.guild(ctx.guild).work_timer()
        timer = timedelta(minutes=timer)
        next_cd = now + timer
        if now.timestamp() < work_stamp:
            #await ctx.send(f"Try again in {}") todo change its
            await ctx.send(f"On cooldown until {humanize_timedelta(timedelta=timer - now)}")
            return
        else:
            """ Work to earn some cookies """
            r = random.choice(list(self.work.keys()))
            await ctx.send(self.work[r])
            def check(m):
                return m.content.lower() in r and m.guild == ctx.guild and m.author == ctx.author
            try:
                await ctx.bot.wait_for('message', timeout=7, check=check)
            except asyncio.TimeoutError:
                return await ctx.send("Have to work harder than that ...😞")
            value = random.randint(50,500)
            cookie = await self.cv(ctx.author)
            cookie += value
            await self.cd(ctx.author,cookie)
            await ctx.send(f"Well done, you earned ``{value}`` cookies for todays work.😴")
            next_cd = now + timer
            await self.conf.user(member).work_stamp.set(next_cd.timestamp())
        
    @commands.command()
    async def dailytimer(self, ctx, amt: int):
        await self.conf.guild(ctx.guild).daily_timer.set(amt)
        await ctx.send(f"successfully set {amt} hours")
        
    @commands.command()
    async def stealtimer(self, ctx, amt: int):
        await self.conf.guild(ctx.guild).steal_timer.set(amt)
        await ctx.send(f"successfully set {amt} houre")
    
    @commands.command()
    async def worktimer(self, ctx, amt: int):
        await self.conf.guild(ctx.guild).work_timer.set(amt)
        await ctx.send(f" sufcesfully set {amt} minutes")
    
    @_cookie.command()
    async def daily(self, ctx):
        """Daily cookies"""
        member = ctx.author
        now = datetime.utcnow().replace(microsecond=0)
        daily_stamp = await self.conf.user(member).daily_stamp()
        if now.timestamp() < daily_stamp:
            await ctx.send(f"On cooldown until: {datetime.fromtimestamp(daily_stamp)}")
        else:
            cookie = await self.cv(ctx.author)
            cookie += 1000
            await ctx.send(f"Claimed your daily cookies. You have ``{cookie}`` cookies now. Come back in 12 hours.🙄")
            daily_timer = await self.conf.guild(ctx.guild).daily_timer()
            timer = timedelta(hours=daily_timer)
            next_cd = timer + now
            await self.cd(ctx.author,cookie)
            await self.conf.user(member).daily_stamp.set(next_cd.timestamp())
  
    @_cookie.command(name="leaderboard", aliases=['lb', 'cb', 'cookieboard'])
    async def leaderboard(self, ctx):
        """Cookieboards UwU"""
        userinfo = await self.conf.all_users()
        if not userinfo:
            return await ctx.send(bold("Start playing first, then check boards."))
        sorted_acc = sorted(userinfo.items(), key=lambda x: x[1]['cookies'], reverse=True)[:50]
        li = []
        for i, (user_id, account) in enumerate(sorted_acc, start=1):
            user_obj = ctx.guild.get_member(user_id)
            if len(user_obj.display_name) < 13:
                li.append(f"#{i:2}. {user_obj.display_name:<13} {account['cookies']:>15} 🍪")
            else:
                li.append(f"#{i:2}. {user_obj.display_name[:10]:<10}... {account['cookies']:>15} 🍪")
        text = "\n".join(li)
        page_list=[]
        for page_num, page in enumerate(pagify(text, delims=['\n'], page_length=1000), start=1):
            embed=discord.Embed(
                color=await self.color(ctx),
                description=box(f"Cookieboards", lang="prolog") + (box(page, lang="md")),
            )
            embed.set_footer (
                text=f"Page {page_num}/{math.ceil(len(text) / 1000)}",
            )
        page_list.append(embed)
        return await menu(ctx, page_list, DEFAULT_CONTROLS)

    @_cookie.command()
    async def steal(self, ctx, *, member: discord.Member=None):
        """Steal others cookies"""
        if member is None or member == ctx.author:
            msg = "Really, you gonna attempt to steal from yourself?"
            return
        you = await self.cv(ctx.author)
        victim = await self.cv(member)
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
            await self.cd(member,victim)
            await self.cd(ctx.author,you)
            msg = f"💎 You've succesfully stolen ``{percent:.0%}`` cookies from ``{member.name}``. 😱"
        else:
            victim += round(percent * you)
            you -= round(percent * you)
            if you <= 0:
                msg = "You dont have enough cookies."
                return
            await self.cd(member,victim)
            await self.cd(ctx.author,you)
            msg = f"👮‍♂️ You got caught! You paid ``{percent:.0%}`` of your cookies for apologies to ``{member.name}`` 😭"
        await ctx.send(msg)
            
    @_cookie.command()
    async def search(self, ctx):
        """ Search for cookies in random places """
        r = random.sample(list(self.loc.keys()), 3)
        await ctx.send("🔍Chose a location to search from bellow🔎")
        await ctx.send(f"``{r[0]}`` , ``{r[1]}``, ``{r[2]}``")
        def check(m):
            return m.content.lower() in r and m.channel == ctx.channel and m.author == ctx.author
        try:
            msg = await ctx.bot.wait_for('message', timeout=7, check=check)
        except asyncio.TimeoutError:
            return await ctx.send("Can't search if I don't know where.")
        cookie = await self.cv(ctx.author)
        if msg.content.lower() in self.badloc:
            return await ctx.send(self.loc[msg.content.lower()])
        else:
            amt = random.randint(50,200)
            cookie = amt + cookie
            await self.cd(ctx.author,cookie)
            return await ctx.send(self.loc[msg.content.lower()].format(amt))
    