import aiohttp
import discord
import asyncio
import re
from redbot.core import commands, Config
from redbot.core.utils.predicates import MessagePredicate

class Paladins(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    #thanks DevilXD
        self.session = aiohttp.ClientSession()
    def cog_unload(self):
        asyncio.create_task(self.session.close())
          
    """ If you have a name with spaces in it please wrap it in double quotes like so
    .last "my long name"
    Champion names with space can be typed as so instead .kda myname bombking or shalin
    """
          
    # shit rewrite
    @commands.command()
    async def last(self, ctx, player, platform="pc"):
        async with self.session.get(f"https://nonsocial.herokuapp.com/api/lastmatch?player={player}&platform={platform}") as r:
            text = await r.text()
            text = text.replace('-', '|').replace('Match', '|')
            text = re.sub('[()]', '', text)
            text = text.split('| ')
            test = len(text)
            newlist = []
            for i in range(test):
                newlist.append(text[i])
            #build embed
            desc = '\n'.join(newlist)
            e = discord.Embed(
                color=await self.bot.get_embed_color(ctx),
                description=f"{desc}",
            )
            e.set_author(name=f"Paladins: showing last match for {player}", icon_url="https://vignette.wikia.nocookie.net/steamtradingcards/images/7/7d/Paladins_Badge_1.png/revision/latest/top-crop/width/300/height/300?cb=20161215201250")
            e.set_footer(text="Data provided by nonsocial.herokuapp.com")
            await ctx.send(embed=e)
            
    @commands.command()
    async def stalk(self, ctx, player, platform="pc"):
        async with self.session.get(f"https://nonsocial.herokuapp.com/api/stalk?player={player}&platform={platform}") as r:
            text = await r.text()
            text = text.replace('-', '|')
            text = re.sub('[()]', '', text)
            text = text.split('| ')
            test = len(text)
            newlist = []
            for i in range(test):
                newlist.append(text[i])
            #build embed
            desc = '\n'.join(newlist)
            e = discord.Embed(
                color=await self.bot.get_embed_color(ctx),
                description=f"{desc}",
            )
            e.set_author(name=f"Paladins: showing online/offline status for {player}", icon_url="https://vignette.wikia.nocookie.net/steamtradingcards/images/7/7d/Paladins_Badge_1.png/revision/latest/top-crop/width/300/height/300?cb=20161215201250")
            e.set_footer(text="Data provided by nonsocial.herokuapp.com")
            await ctx.send(embed=e)
            
    @commands.command()
    async def current(self, ctx, player, platform="pc"):
        async with self.session.get(f"https://nonsocial.herokuapp.com/api/live_match?player={player}&platform={platform}") as r:
            text = await r.text()
            text = text.replace('-', '|').replace(',', '|')
            text = re.sub('[()]', '', text)
            text = text.split('| ')
            test = len(text)
            newlist = []
            for i in range(test):
                newlist.append(text[i])
            #build embed
            desc = '\n'.join(newlist)
            e = discord.Embed(
                color=await self.bot.get_embed_color(ctx),
                description=f"{desc}",
            )
            e.set_author(name=f"Paladins: showing current match for {player}", icon_url="https://vignette.wikia.nocookie.net/steamtradingcards/images/7/7d/Paladins_Badge_1.png/revision/latest/top-crop/width/300/height/300?cb=20161215201250")
            e.set_footer(text="Data provided by nonsocial.herokuapp.com")
            await ctx.send(embed=e)
            
    @commands.command()
    async def rank(self, ctx, player, platform="pc"):
        async with self.session.get(f"https://nonsocial.herokuapp.com/api/rank?player={player}&platform={platform}") as r:
            text = await r.text()
            text = text.replace('-', '|')
            text = re.sub('[()]', '', text)
            text = text.split('| ')
            test = len(text)
            newlist = []
            for i in range(test):
                newlist.append(text[i])
            #build embed
            desc = '\n'.join(newlist)
            e = discord.Embed(
                color=await self.bot.get_embed_color(ctx),
                description=f"{desc}",
            )
            e.set_author(name=f"Paladins: showing rank for {player}", icon_url="https://vignette.wikia.nocookie.net/steamtradingcards/images/7/7d/Paladins_Badge_1.png/revision/latest/top-crop/width/300/height/300?cb=20161215201250")
            e.set_footer(text="Data provided by nonsocial.herokuapp.com")
            await ctx.send(embed=e)
            
    @commands.command()
    async def kda(self, ctx, player, champion="", platform="pc"):
        async with self.session.get(f"https://nonsocial.herokuapp.com/api/kda?player={player}&champion={champion}&platform={platform}") as r:
            text = await r.text()
            text = text.replace('-', '|')
            text = re.sub('[()]', '', text)
            text = text.split('| ')
            test = len(text)
            newlist = []
            for i in range(test):
                newlist.append(text[i])
            #build embed
            desc = '\n'.join(newlist)
            e = discord.Embed(
                color=await self.bot.get_embed_color(ctx),
                description=f"{desc}",
            )
            e.set_author(name=f"Paladins: showing kill/death/assist ratio for {player}", icon_url="https://vignette.wikia.nocookie.net/steamtradingcards/images/7/7d/Paladins_Badge_1.png/revision/latest/top-crop/width/300/height/300?cb=20161215201250")
            e.set_footer(text="Data provided by nonsocial.herokuapp.com")
            await ctx.send(embed=e)
            