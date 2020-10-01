import apsw
import discord
import random
import math
import asyncio
from textwrap import dedent
from redbot.core import commands
from tabulate import tabulate
from datetime import datetime, timedelta
from redbot.core.data_manager import cog_data_path
from redbot.core.utils.chat_formatting import humanize_timedelta
from redbot.core.utils.predicates import MessagePredicate
from .random import worklist, searchlist, petlist, bad_loc
from .taskhelper import TaskHelper


class Coin(TaskHelper, commands.Cog):
    """Coin Tycoon game by mucski"""
    def __init__(self, bot):
        self.bot = bot
        TaskHelper.__init__(self)
        self.db = Config.get_conf(self, 49348238760987, force_registration=True)
        
        default_user = {
            "data": {} #{potato: 0, and more}
        }
        default_guild = {
            "guild_data": {} #{channel: and more}
        }
        self.db.register_user(**default_user)
        self.db.register_guild(**default_guild)

    @commands.group(aliases=['c'])
    async def coin(self, ctx):
        pass

    @coin.command(aliases=['bal'])
    async def balance(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        async with self.db.user(ctx.member).data() as data:
            if bool(data) is False:
                await ctx.send("You need to start playing first. To do so claim your first daily by typing in .daily")
                return
            coin = data['coin']
            await ctx.send(f"{ctx.member} has {coin} coins.")
            
    @coin.command()
    async def daily(self, ctx):
        async with self.db.user(ctx.author).data() as data:
            now = datetime.utcnow()
            try:
                stamp = data['dailystamp']
                stamp = datetime.fromtimestamp(stamp)
            except KeyError:
                stamp = now
            data['coin'] = 300
            future =  now + timedelta(hours=12)
            data['dailystamp'] = future.timestamp()
            if stamp > now:
                await ctx.send(f"You already claimed your daily coins. Check back in {humanize.naturaldelta(stamp - now)}")
                return
            await ctx.send("Claimed 300 coins. Check back in 12 hours.")

    @coin.command()
    @commands.cooldown(1, 11, commands.BucketType.user)
    async def work(self, ctx):
        if self.check_player(ctx.author.id) is None:
            await ctx.send("Start playing first by claiming daily.")
            return
        r = random.choice(list(worklist.keys()))
        await ctx.send(worklist[r])
        pred = MessagePredicate.lower_equal_to(r, ctx)
        try:
            await ctx.bot.wait_for('message', timeout=10, check=pred)
        except asyncio.TimeoutError:
            await ctx.send("You failed to work. You are fired. Just kidding.")
            return
        earned = random.randint(5, 30)
        self.add_coin(earned, ctx.author.id)
        await ctx.send(f"Well done, you earned ``{earned}`` for your hard work.")

    @coin.command()
    @commands.cooldown(1, 11, commands.BucketType.user)
    async def search(self, ctx):
        if self.check_player(ctx.author.id) is False:
            await ctx.send("Start playing first by claiming your first daily coins.")
            return
        r = random.sample(list(searchlist.keys()), 3)
        await ctx.send("Chose a random location to search from bellow\n"
        			   "``{}`` , ``{}`` , ``{}``".format(r[0],r[1],r[2]))
        check = MessagePredicate.lower_contained_in(r,ctx)
        try:
            msg = await ctx.bot.wait_for("message", timeout=10, check=check)
        except asyncio.TimeoutError:
            await ctx.send("Epic fail!")
            return
        if msg.content.lower() in bad_loc:
            await ctx.send(searchlist[msg.content.lower()])
            return
        else:
            earned = random.randint(5, 30)
            self.add_coin(earned, ctx.author.id)
            await ctx.send(searchlist[msg.content.lower()].format(earned))

    @coin.command()
    async def gamble(self, ctx, amt: int):
        you = random.randint(1, 6)
        dealer = random.randint(1, 6)
        if amt < 0:
            await ctx.send("Cant gamble nothing")
            return
        if self.check_player(ctx.author.id) is None:
            await ctx.send("Start playing first by claiming your first daily coins")
            return
        coin = self.select_one("coin", "users", "user_id", ctx.author.id)
        if amt > coin[0]:
            await ctx.send("You don't have that much coins.")
            return
        #Build an EMBED!
        embed = discord.Embed(color = await self.bot.get_embed_color(ctx), title = "Roll the Dice.")
        if you > 6 or dealer < you:
            embed.add_field(name = "Dealer rolled:", value = f"🎲 {dealer}")
            embed.add_field(name = "You rolled:", value = f"🎲 {you}")
            embed.description = "YOU WON!"
            self.add_coin(amt, ctx.author.id)
        elif you == dealer:
            embed.add_field(name = "Dealer rolled:", value = f"🎲 {dealer}")
            embed.add_field(name = "You rolled:", value = f"🎲 {you}")
            embed.description = "It's a tie."
        elif you < 6 or dealer > you:
            embed.add_field(name = "Dealer rolled:", value = f"🎲 {dealer}")
            embed.add_field(name = "You rolled:", value = f"🎲 {you}")
            embed.description = "YOU LOST!"
            self.remove_coin(amt, ctx.author.id)
        embed.set_footer(text = "Roll the dice, whoever has the highest wins.")
        await ctx.send(embed = embed)
                    
    @coin.command(aliases = ["lb"])
    async def leaderboard(self, ctx):
        c = self.db.cursor()
        c.execute("SELECT * FROM users ORDER BY coin DESC")
        users = []
        for i, row in enumerate(c, start=1):
            rows = []
            name = f"{row[1]}"
            coin = f"{row[3]}"
            rows.append(f"{i}")
            rows.append(name)
            rows.append(coin)
            users.append(rows)
        table = tabulate(users, headers = ['#', 'Name', 'Coin'], numalign = 'right', tablefmt = 'presto')
        embed = discord.Embed(color = await self.bot.get_embed_color(ctx), title = "Leaderboards")
        embed.description = f"```{table}```"
        embed.set_footer(text = f"Top 50 players on {ctx.guild.name}")
        await ctx.send(embed = embed)
        
    @coin.command()
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def dig(self, ctx):
        if self.check_player(ctx.author.id) is None:
            await ctx.send("Start playing first by claiming your first daily. ")
            return
            
        chest = random.randint(1, 64)
        
        desc = """
        NW + -- + -- + -- N -- + -- + -- + NE
        01 | 02 | 03 | 04 | 05 | 06 | 07 | 08 
        -- + -- + -- + -- + -- + -- + -- + --
        09 | 10 | 11 | 12 | 13 | 14 | 15 | 16
        -- + -- + -- + -- + -- + -- + -- + --
        17 | 18 | 19 | 20 | 21 | 22 | 23 | 24
        -- + -- + -- + -- + -- + -- + -- + --
        25 | 26 | 27 | 28 | 29 | 30 | 31 | 32
        W  + -- + -- + -- o -- + -- + -- +  E
        33 | 34 | 35 | 36 | 37 | 38 | 39 | 40
        -- + -- + -- + -- + -- + -- + -- + --
        41 | 42 | 43 | 44 | 45 | 46 | 47 | 48
        -- + -- + -- + -- + -- + -- + -- + --
        49 | 50 | 51 | 52 | 53 | 54 | 55 | 56
        -- + -- + -- + -- + -- + -- + -- + --
        57 | 58 | 59 | 60 | 61 | 62 | 63 | 64
        SW + -- + -- + -- S -- + -- + -- + SE
        """
        north = [4, 5, 12, 13, 20, 21, 28, 29]
        north_west = [1, 2, 3, 9, 10, 11, 17, 18, 19]
        north_east = [6, 7, 8, 14, 15, 16, 22, 23, 24]
        west = [25, 26, 27, 28, 29, 30, 35, 36]
        south_west = [41, 42, 43, 49, 50, 51, 57, 58, 59]
        south_east = [46, 47, 48, 54, 55, 56, 62, 63, 64]
        south = [36, 44, 52, 60, 61, 53, 45, 37]
        east = [29, 30, 31, 32, 37, 38, 39, 40]
        
        if chest in north:
            hint = "North"
        elif chest in north_west:
            hint = "North West"
        elif chest in north_east:
            hint = "North East"
        elif chest in west:
            hint = "West"
        elif chest in south_west:
            hint = "South West"
        elif chest in south_east:
            hint = "South East"
        elif chest in south:
            hint = "South"
        elif chest in east:
            hint = "East"
        else:
            hint = "None"
            
        embed = discord.Embed(
            color = await self.bot.get_embed_color(ctx), 
            description = f"Chose a number between 1 and 64```{dedent(desc)}```Hint: Your compass points towards {hint}", 
            title = "Find the pirate booty chest!"
        )
        await ctx.send(embed = embed)
            
        pred = MessagePredicate.same_context(ctx)
        try:
            msg = await ctx.bot.wait_for("message", timeout = 20, check = pred)
        except asyncio.TimeoutError:
            await ctx.send("Can't dig nowhere, you need to input a number or 'random' if you are too lazy.")
            return
            
        your_input = msg.content.lower()
            
        try:
            your_input = int(msg.content)
        except ValueError:
            if your_input == "random":
                your_input = random.randint(1, 64)
            else:
                await ctx.send("Wrong input type.")
                return
            
        if math.isclose(your_input, chest, rel_tol = 0.1) is True:
            earned = random.randint(20, 50)
            self.add_coin(earned, ctx.author.id)
            await ctx.send(f"You were close, but not really\nFound a small chest with ``{earned}`` coins in it.\nYou can't help but wonder what kind of treasures the big one could contain...")
            return
        elif your_input == chest:
            self.add_coin(1000, ctx.author.id)
            await ctx.send(f"You found it!\nThe treasure chest contained ``{earned}`` coins")
            return
        else:
            await ctx.send("Not even close, you found nothing.")
            return

    @coin.group(invoke_without_command = True)
    async def shop(self, ctx):
        await ctx.send("Use ``.coin shop items`` to view items and ``.coin shop pets`` to view available pets.")

    @shop.command()
    async def pets(self, ctx):
        embed = discord.Embed(color = await self.bot.get_embed_color(ctx))
        embed.set_author(name = f"{self.bot.user.name}' pet shop.", icon_url = self.bot.user.avatar_url)
        for k, v in petlist.items():
            #Build embed
            embed.add_field(name = "Name", value = f"{v['emoji']} **{k.capitalize()}**")
            embed.add_field(name = "Description", value = f"_{v['description']}_")
            embed.add_field(name = "Price", value = f"``{v['price']}``")
        embed.set_footer(text = "To buy a pet do .coin shop buy [petname]")
        await ctx.send(embed=embed)
        
    @shop.command()
    async def items(self, ctx):
        pass
    
    @coin.group(invoke_without_command = True)
    async def pet(self, ctx):
        pass
    
    @pet.command()
    async def buy(self, ctx, pet: str):
        if self.check_player(ctx.author.id) is None:
            await ctx.send("You need to start playing first before thinking on buying a pet.")
            return
        if pet in petlist:
            coin = self.select_one("coin", "users", "user_id", ctx.author.id)
            if coin[0] < petlist['price']:
                await ctx.send("You don't have enough coins to buy that pet.")
                return
            if coin[0] - petlist['price'] <= 0:
                await ctx.send("You don't have enough coins to buy that pet.")
                return
            self.remove_coin(petlist['price'], ctx.author.id)
            c = self.db.cursor()
            c.execute(f"INSERT INTO pets (user_id, pet_hunger, pet_clean, pet_happy, pet_name, pet_type) VALUES (?,?,?,?,?,?)",(ctx.author.id, 100, 100, 100, pet, pet))
            await ctx.send(f"Congrats, you own a {pet.capitalize()} now. Take good care of it.")
        else:
            await ctx.send("No such pet.")
        
    @pet.command()
    async def info(self, ctx):
        if self.check_player(ctx.author.id) is None:
            await ctx.send("You cannot check your pet when you didn't even start playing yet. Start playing by claiming your first daily.")
            return
        c = self.db.cursor()
        c.execute("SELECT * FROM pets WHERE user_id = ?",(ctx.author.id,))
        pet = c.fetchone()
        if pet[5] == "cat":
            emoji = ":cat:"
        if pet[5] == "dog":
            emoji = ":dog:"
        if pet[5] == "turtle":
            emoji = ":turtle:"
        if pet[5] == "rock":
            emoji = ":moyai:"
        embed = discord.Embed(color = await self.bot.get_embed_color(ctx))
        embed.set_author(name = f"{ctx.author.name}'s pet info", icon_url = ctx.author.avatar_url)
        embed.add_field(name = "Pet Name", value = pet[4].capitalize(), inline = False)
        embed.add_field(name = "Pet Type", value = f"{emoji} ({pet[5]})", inline = False)
        embed.add_field(name = "Pet Hunger", value = pet[1], inline = False)
        embed.add_field(name = "Pet Clean", value = pet[2], inline = False)
        embed.add_field(name = "Pet Happy", value = pet[3], inline = False)
        embed.set_footer(text = "Take good care of your pet.")
        await ctx.send(embed = embed)