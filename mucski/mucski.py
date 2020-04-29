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
        }
        self.badloc = ['fridge','dog','toilet']
        self.work = {
            "hot dog":"You are working outside with a cart. Un scramble the following word ``dot goh``", 
            "cauterize": "You're a pro Paladins player. What do you buy first at match start? ", 
            "covid19": "You can't work cause of Quarantine. Kill the virus ``c _ _ _ _ _ _``",
            "jack sparrow": "You're a famous Pirate. Who are you?", 
            "bulbbulb": "Type the following word in reverse ``blubblub``", 
            "dick": "You are working as a professional hunter. Shot the u out of a duck.",
            "redbot": "I'm a bot, but do you know my name?",
            "mucski": f"Had to include it here ... Unscramble me. ``{self.shuffle_word('mucski')}``",
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
        if self.bot.get_command('cookie daily').is_on_cooldown(ctx) == True:
            cooling = "Yes"
        else:
            cooling = "No"
        #build embed
        e = discord.Embed(color=await self.color(ctx))
        e.set_author(name=f"Profile for {member.name}", icon_url=member.avatar_url)
        e.set_thumbnail(url=member.avatar_url)
        e.add_field(name="Cookies owned", value=f"``{cookie}``")
        e.add_field(name="Daily on cooldown", value=f"``{cooling}``")
        e.set_image(url="")
        e.set_footer(text=datetime.datetime.utcnow())
        await ctx.send(embed=e)
        
    @_cookie.command()
    async def gamble(self, ctx, amount):
        """ Gamble amount of cookies with a chance to win double """
        cookie = await self.cv(ctx.author)
        try:
            amount = int(amount)
        except ValueError:
            if amount == 'all':
                amount = cookie
            else:
                amount = None
                msg= "Can't gamble what you don't have."
        finally:
            if amount is not None:
                if cookie - abs(amount) < 0:
                    msg = "Go get yourself some cookies then try again."
                elif amount <= 0:
                    msg = "Invalid number of cookies."
                else:
                    if random.random() < 0.3:
                        winning = amount*2
                        cookie += winning
                        await self.cd(ctx.author,cookie)
                        msg = f"Congratulations ``{ctx.author.name}`` you won ``{winning}`` cookies 🍪🎉"
                    else:
                        cookie -= amount
                        await self.cd(ctx.author,cookie)
                        msg = f"Oops, you lost ``{amount}`` cookies. 😞"
        await ctx.send(msg)
        
    @_cookie.command()
    async def roll(self, ctx, amount):
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
                if cookie - abs(amount) < 0:
                    msg = "Get yourself some cookies first"
                elif amount <= 0:
                    msg = "Invalid amount of cookies!"
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
        embed.add_field(name="Dealer rolled", value=dealer)
        embed.add_field(name="You rolled", value=member)
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
    @commands.cooldown(rate=1, per=100, type=commands.BucketType.user)
    async def work(self, ctx):
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
        return await ctx.send(f"Well done, you earned ``{value}`` cookies for todays work.😴")
    
    @_cookie.command(cooldown_after_parsing=True)
    @commands.cooldown(rate=1, per=43200, type=commands.BucketType.user)
    async def daily(self, ctx):
        """Daily cookies"""
        cookie = await self.cv(ctx.author)
        cookie += 1000
        await self.cd(ctx.author,cookie)
        await ctx.send(f"Claimed your daily cookies. You have ``{cookie}`` cookies now. Come back in 12 hours.🙄")
  
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
            msg = f"You've succesfully stolen ``{percent:.0%}`` cookies from ``{member.name}``.😱"
        else:
            victim += round(percent * you)
            you -= round(percent * you)
            if you <= 0:
                msg = "You dont have enough cookies."
                return
            await self.cd(member,victim)
            await self.cd(ctx.author,you)
            msg = f"You got caught! You paid ``{percent:.0%}`` of your cookies for apologies to ``{member.name}``😭"
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
    