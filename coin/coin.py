import discord
import asyncio
from redbot.core.utils.predicates import MessagePredicate, ReactionPredicate
from redbot.core import commands, Config, checks
import random
from math import floor, ceil, isclose
from .random import worklist, searchlist, bad_loc
from textwrap import dedent
from redbot.core.utils.chat_formatting import pagify, box
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
from redbot.core.utils.menus import start_adding_reactions


class Coin(commands.Cog):
    """Coin Tycoon game by mucski"""
    def __init__(self, bot):
        self.bot = bot
        self.db = Config.get_conf(self, 9769879876, force_registration=True)

        default_user = {
            "coin": 0,
            "dailystamp": 0,
            "stealstamp": 0,
        }
        
        default_guild = {
            "channel": "",
        }
        
        self.db.register_user(**default_user)
        self.db.register_guild(**default_guild)
        self.playing = False
        self.cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]*4
        
    @commands.hybrid_group()
    async def coin(self, interaction: discord.Interaction):
        """ Coin Tycoon created by Mucski \n
            The point of the game is to have as much coins as you can.
            You can earn coins by working, searching, claiming daily
            stealing, gambling (and more coming soon). \n
            See the commands bellow to get started.
        """
        pass

    @coin.command(aliases=['bal'])
    async def balance(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        else:
            member = member
        coin = await self.db.user(member).coin()
        await ctx.send(f"{member.mention} has {coin} coins.")

    @coin.command()
    @commands.cooldown(1, 43200, commands.BucketType.user)
    async def daily(self, ctx):
        if not self.playing:
            self.playing = True
        coin = await self.db.user(ctx.author).coin()
        coin += 300
        await self.db.user(ctx.author).coin.set(coin)
        await ctx.send("Claimed 300 coins. Check back in 12 hours.")
    
    @coin.command()
    @checks.is_owner()
    async def resetdaily(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author
        await self.db.user(member).dailystamp.clear()
        await ctx.send(f"Cleared {member.display_name}'s daily cooldown timer.")
        
    @coin.command()
    @checks.is_owner()
    async def resetsteal(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author
        await self.db.user(member).stealstamp.clear()
        await ctx.send(f"Cleared {member.display_name}'s steal cooldown timer.")
        
    @coin.command()
    @checks.is_owner()
    async def setcoin(self, ctx, amt: int, member: discord.Member = None):
        if not member:
            member = ctx.author
        coin = await self.db.user(member).coin()
        coin = amt
        await self.db.user(member).coin.set(coin)
        await ctx.send(f"Set {member.display_name}'s coin to {amt}")

    @coin.command()
    @commands.cooldown(1, 11, commands.BucketType.user)
    async def work(self, ctx):
        coin = await self.db.user(ctx.author).coin()
        if coin == 0 and not self.playing:
            await ctx.send("Start playing first by claiming daily.")
            return
        r = random.choice(list(worklist.keys()))
        await ctx.send(worklist[r])
        pred = MessagePredicate.lower_equal_to(r, ctx)
        try:
            await ctx.bot.wait_for('message', timeout=15, check=pred)
        except asyncio.TimeoutError:
            await ctx.send("You failed to work. You are fired. Just kidding.")
            return
        earned = random.randint(5, 30)
        coin += earned
        await self.db.user(ctx.author).coin.set(coin)
        await ctx.send(f"Well done, you earned `{earned}` for your hard work.")

    @coin.command()
    @commands.cooldown(1, 11, commands.BucketType.user)
    async def search(self, ctx):
        coin = await self.db.user(ctx.author).coin()
        if coin == 0 and not self.playing:
            await ctx.send("Start playing first by claiming daily.")
            return
        r = random.sample(list(searchlist.keys()), 3)
        await ctx.send("Chose a random location to search from bellow\n"
                       "`{}` , `{}` , `{}`".format(r[0], r[1], r[2]))
        check = MessagePredicate.lower_contained_in(r, ctx)
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
            coin += earned
            await self.db.user(ctx.author).coin.set(coin)
            await ctx.send(searchlist[msg.content.lower()].format(earned))

    @coin.command()
    @commands.cooldown(1, 11, commands.BucketType.user)
    async def gamble(self, ctx, amt: int):
        you = random.randint(1, 12)
        dealer = random.randint(1, 12)
        coin = await self.db.user(ctx.author).coin()
        if amt < 0:
            await ctx.send("Can't gamble nothing")
            return
        if coin == 0 and not self.playing:
            await ctx.send("Start playing first by claiming daily.")
            return
        if amt > coin:
            await ctx.send("You don't have that much coins.")
            return
        # Build an EMBED!
        embed = discord.Embed(color=await self.bot.get_embed_color(ctx),
                              title="Roll the Dice.")
        if you > 12 or dealer < you:
            embed.add_field(name="Dealer rolled:", value=f"🎲 {dealer}")
            embed.add_field(name="You rolled:", value=f"🎲 {you}")
            embed.description = "YOU WON!"
            coin += amt
            await self.db.user(ctx.author).coin.set(coin)
        elif you == dealer:
            embed.add_field(name="Dealer rolled:", value=f"🎲 {dealer}")
            embed.add_field(name="You rolled:", value=f"🎲 {you}")
            embed.description = "It's a tie."
        elif you < 12 or dealer > you:
            embed.add_field(name="Dealer rolled:", value=f"🎲 {dealer}")
            embed.add_field(name="You rolled:", value=f"🎲 {you}")
            embed.description = "YOU LOST!"
            coin -= amt
            await self.db.user(ctx.author).coin.set(coin)
        embed.set_footer(text="Roll the dice, whoever has the highest wins.")
        await ctx.send(embed=embed)

    @coin.command(aliases=['lb'])
    async def leaderboard(self, ctx):
        userinfo = await self.db.all_users()
        if not userinfo:
            return await ctx.send("Start playing first, then check boards.")
        sorted_acc = sorted(userinfo.items(), key=lambda x: x[1]['coin'],
                            reverse=True)[:50]
        li = []
        for i, (user_id, account) in enumerate(sorted_acc, start=1):
            user_obj = ctx.guild.get_member(user_id)
            if user_obj is None:
                continue
            li.append(f"#{i:2} {user_obj.display_name:<15}"
                      f"{account['coin']:>15}")
        text = "\n".join(li)
        page_list = []
        for page_num, page in enumerate(pagify(text, delims=['\n'],
                                        page_length=1000), start=1):
            embed = discord.Embed(
                color=await ctx.bot.get_embed_color(location=ctx.channel),
                description=box("Leaderboards",
                                lang="prolog") + (box(page, lang="md")),
            )
            embed.set_footer(
                text=f"Page {page_num}/{ceil(len(text) / 1000)}",
            )
        page_list.append(embed)
        return await menu(ctx, page_list, DEFAULT_CONTROLS)

    @coin.command()
    @commands.cooldown(1, 21600, commands.BucketType.user)
    async def steal(self, ctx, member: discord.Member):
        self_coin = await self.db.user(ctx.author).coin()
        enemy_coin = await self.db.user(member).coin()
        if enemy_coin == 0:
            await ctx.send(f"Poor {member.display_name} has nothing left to steal or haven't started playing yet.")
            return
        if member == ctx.author:
            await ctx.send("Do you really want to rob yourself?")
            return
        emojis = ["◀", "▶", "❌"]
        chars = "◀▶◀▶◀▶◀▶◀▶"
        var = 0
        key = 3
        pick = []
        chars = list(chars)
        random.shuffle(chars)
        chars = ''.join(chars)

        e = discord.Embed(title=f"{ctx.author.name}"
                                f" is stealing from {member.display_name}")
        try:
            e.set_thumbnail(url=member.avatar.url)
        except AttributeError:
            pass
        e.add_field(name="\u200b",
                    value="If you run out of picks, you lost."
                          "\nLockpicks left: **3**", inline=False)
        e.description = (
            "```\n___________\n```"
        )
        # e.add_field(name="\u200b", value="Lockpicks left: 3", inline=False)
        e.set_footer(text="Pick the lock using the ◀ and ▶ and ❌ to cancel.")
        msg = await ctx.send(embed=e)
        start_adding_reactions(msg, emojis)
        while True:
            pred = ReactionPredicate.with_emojis(emojis, message=msg,
                                                 user=ctx.author)
            try:
                await ctx.bot.wait_for("reaction_add", check=pred, timeout=60)
            except asyncio.TimeoutError:
                await msg.clear_reactions()
                break
            emoji = emojis[pred.result]
            if emoji == '❌':
                await msg.clear_reactions()
                e.description = "```\nYou cancelled.\n```"
                await msg.edit(embed=e)
                break
            # elif emoji == '▶️':
            #    direction = ">"
            # elif emoji == '◀️':
            #    direction = "<"
            if emoji == chars[var]:
                try:
                    var += 1
                    line = "__________"
                    pick.append(emoji)
                    e.description = (
                        "```\n{}\n```".format(''.join(pick) + line[var:])
                    )
                    await msg.edit(embed=e)
                except IndexError:
                    break
            else:
                try:
                    key -= 1
                    e.set_field_at(0, name="\u200b",
                                   value=f"If you run out of picks"
                                         f", you lost.\nLockpicks left:"
                                         f" **{key}**", inline=False)
                    await msg.edit(embed=e)
                except IndexError:
                    break
            if var == 10 or key == 0:
                percent = var * 5
                stolen = enemy_coin * percent // 100
                e.set_field_at(0, name="\u200b",
                               value=f"You successfully stolen"
                               f" `{percent}%` of "
                               f"{member.display_name}'s coins."
                               f"\nYou earned `{stolen}` coins.\n"
                               f"Lockpicks left: **{key}**", inline=False)
                await msg.edit(embed=e)
                self_coin += stolen
                enemy_coin -= stolen
                await self.db.user(ctx.author).coin.set(self_coin)
                await self.db.user(member).coin.set(enemy_coin)
                break
            try:
                await msg.remove_reaction(emoji, ctx.author)
            except discord.HTTPException:
                pass

    @coin.command()
    async def bj(self, ctx):
        def deal(cards):
            hand = []
            for i in range(2):
                random.shuffle(cards)
                card = self.cards.pop()
                if card == 11: card = "J"
                if card == 12: card = "Q"
                if card == 13: card = "K"
                if card == 14: card = "A"
                hand.append(card)
            return hand
            
        def total(hand):
            total = 0
            for card in hand:
                if card == "J" or card == "Q" or card == "K":
                    total += 10
                elif card == "A":
                    if total >= 11: total += 1
                    else: total += 11
                else:
                    total += card
            return total
            
        def hit(hand):
            card = self.cards.pop()
            if card == 11: card = "J"
            if card == 12: card = "Q"
            if card == 13: card = "K"
            if card == 14: card = "A"
            hand.append(card)
            return hand
        
        def score(dealer_hand, player_hand):
            if total(player_hand) == 21:
                msg = "Congratulations you won, you have a Black Jack"
            elif total(dealer_hand) == 21:
                msg = "Sorry, you lose, I got a Black Jack"
            elif total(player_hand) > 21:
                msg = "Ha! You bust! I win!"
            elif total(dealer_hand) > 21:
                msg = "Oops, looks like I'm bust, you win!"
            elif total(player_hand) < total(dealer_hand):
                msg = "Ha! I have more, so I win"
            elif total(player_hand) > total(dealer_hand):
                msg = "Looks like you have more than me, you won!"
                
        await ctx.send("Welcome to BlackJack, I don't have time to explain the rules")
        
        quit = False
        
        while not quit:
            player_hand = deal(self.cards)
            dealer_hand = deal(self.cards)
            
            await ctx.send("I have a " + str(dealer_hand[0]))
            await ctx.send("You have a " + str(player_hand[0]) + " and a " + str(player_hand[1]) + " for a total of " + str(total(player_hand)))
            await ctx.send("Do you want to [H]it, [S]tand or [Q]uit")
            
            msg = await self.bot.wait_for("message", check=MessagePredicate.same_context(ctx))
            
            if msg.content.lower() == "h":
                hit(player_hand)
                await ctx.send("Player hand: " + str(player_hand))
                await ctx.send("Hand total" + str(total(player_hand)))
                if total(player_hand) > 21:
                    "You're bust, you lost!"
                    quit = True
            elif msg.content.lower() == "s":
                while total(dealer_hand) < 17:
                    hit(dealer_hand)
                    await ctx.send("Dealer hand: " str(dealer_hand))
                    if total(dealer_hand) > 21:
                        await ctx.send("Oops, looks like you won")
                        quit = True
                score(player_hand, dealer_hand)
            elif msg.content.lower() == "q":
                quit = True
                await ctx.send("Bye")
                    
    @coin.command()
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def dig(self, ctx, cheat=False):
        coin = await self.db.user(ctx.author).coin()
        if coin == 0 and not self.playing:
            await ctx.send("Start playing first by claiming daily.")
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
            color=await self.bot.get_embed_color(ctx),
            description=f"Chose a number between 1 and 64"
                        f"```{dedent(desc)}```Hint: Your compass "
                        f"points towards {hint}",
            title="Find the pirate booty chest!"
        )
        
        if chest <= 9 and len(str(chest)) < 2:
            chest_str = "0" + str(chest)
        else:
            chest_str = str(chest)
        
        desc2 = desc.replace(chest_str, "❌", 1)
        embed2 = discord.Embed(
            color=await self.bot.get_embed_color(ctx),
            description=f"```{dedent(desc2)}```",
            title="The chest was here!"
        )
        await ctx.send(embed=embed)
        if cheat:
            if await self.bot.is_owner(ctx.author):
                await ctx.send(f"Pst, the chest is here {chest}")
            else:
                pass

        pred = MessagePredicate.same_context(ctx)
        try:
            msg = await ctx.bot.wait_for("message", timeout=20, check=pred)
        except asyncio.TimeoutError:
            await ctx.send("Can't dig nowhere, you need to input a number "
                           "or 'random' if you are too lazy.")
            return

        your_input = msg.content.lower()

        try:
            your_input = int(msg.content)
        except ValueError:
            await ctx.send("Wrong input type. Try again, but this time with numbers.")
            return
        
        if your_input == chest:
            coin += 1000
            await self.db.user(ctx.author).coin.set(coin)
            try:
                await msg.edit(embed=embed2)
            except discord.errors.Forbidden:
                await ctx.send(embed=embed2)
            await ctx.send("You found it!\nThe treasure"
                           "chest contained `1000` coins")
            return
        elif isclose(your_input, chest, rel_tol=0.1) is True:
            earned = random.randint(20, 50)
            coin += earned
            await self.db.user(ctx.author).coin.set(coin)
            try:
                await msg.edit(embed=embed2)
            except discord.errors.Forbidden:
                await ctx.send(embed=embed2)
            await ctx.send(f"You were close, but not really\n"
                           f"Found a small chest with `{earned}`"
                           f" coins in it.\n"
                           f"You can't help but wonder what kind of treasures "
                           f"the big one could contain...")
            return
        else:
            try:
                await msg.edit(embed=embed2)
            except discord.errors.Forbidden:
                await ctx.send(embed=embed2)
            await ctx.send("You found nothing!")
            return
