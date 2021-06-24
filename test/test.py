from redbot.core import commands
import random
from redbot.core.utils.menus import start_adding_reactions
from redbot.core.utils.predicates import ReactionPredicate
import discord
import asyncio


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def test(self, ctx):
        pass

    @test.command()
    async def lockpick(self, ctx, number: int):
        emojis = ["◀", "▶", "❌"]
        chars = "◀▶"
        var = 0
        key = 3
        lock_length = 10
        pick = []
        line = "__________"
        lock = ''.join(random.choice(chars) for _ in range(lock_length))
        desc = (
            "Steal someone's coins by pressing < or > like a retard\n"
            "Lockpicks left: 3"
            f"{line}"
        )
        embed = discord.Embed(title="Stealing from your mom", description=desc)
        embed.set_footer(text="Pick the lock using the ◀ and ▶ and ❌ to cancel.")
        msg = await ctx.send(embed=embed)
        start_adding_reactions(msg, emojis)

        while True:
            pred = ReactionPredicate.with_emojis(emojis, message=msg, user=ctx.author)
            try:
                await ctx.bot.wait_for("reactions_add", check=pred, timeout=60)
            except asyncio.TimeoutError:
                await msg.clear_reactions()
                return
            emoji = emojis[pred.result]
            if emoji == '❌':
                await msg.clear_reactions()
                embed.description = "You have cancelled. GG"
                msg.edit(embed=embed)
                break
            if emoji == chars[var]:
                try:
                    var+1
                    line = "__________"
                    pick.append(emoji)
                    line = ''.join(pick) + line[var:]
                    msg.edit(embed)
                except IndexError:
                    break
