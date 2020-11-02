from redbot.core import commands
import random
from .words import words, words2

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def whoami(self, ctx):
        word = random.choice(words)
        word2 = random.choice(words2)
        await ctx.send(f"{word} {word2}")
        
    async def on_message(message):
        if message.content.startswith("thttps://cdn.discordapp.com/attachments/760415177459105803/772901957030903818/20201102_093922.jpg")
            await ctx.send("https://cdn.discordapp.com/attachments/760415177459105803/772901957030903818/20201102_093922.jpg")
        else
            pass
