import discord
import random

from redbot.core import commands, checks

class Games(commands.Cog):
    
    @commands.group(name="coin", aliases=['c'], pass_context=True)
    async def coin(self, ctx)
    
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
        