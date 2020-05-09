import aiohttp
import discord
import asyncio
import re
from redbot.core import commands, Config
from redbot.core.utils.predicates import MessagePredicate

class Paladins(commands.Cog):
    """ If you have a name with spaces in it please wrap it in double quotes like so .last "my long name"
    Champion names with space can be typed as so instead .kda myname bombking or shalin"""
    def __init__(self, bot):
        self.bot = bot
    #thanks DevilXD
        self.session = aiohttp.ClientSession()
    def cog_unload(self):
        asyncio.create_task(self.session.close())
           
    # shit rewrite
    @commands.command()
    async def last(self, ctx, player, platform="pc"):
        """Shows last played match by ``player``"""
        async with self.session.get(f"https://nonsocial.herokuapp.com/api/lastmatch?player={player}&platform={platform}") as r:
            text = await r.text()
            #pain im the ass regex, domt touch
            text = re.findall(r"([\w]+\s[\w|\s]+).*Id:\s(\d+).*ation:\W+(\d+)m.*ion:\s([\w|\s🇺🇸]+)\W+([\w|\w\s]+)\W+([\d/]+)\W+([\d.]+).*ee:\s(\d+).*ge:\s([\d,]+).*its:\s([\d,]+).*re:\s([\d/]+)", text)
            avatar = text[0][4].replace(' ', '-')
            avatarurl = f"https://web2.hirez.com/paladins/champion-icons/{avatar.lower()}.jpg"
            e = discord.Embed(color=await self.bot.get_embed_color(ctx))
            e.set_thumbnail(url=avatarurl)
            e.add_field(name="Map", value=text[0][0])
            e.add_field(name="Match Id:", value=text[0][1])
            e.add_field(name="Duration", value=text[0][2])
            e.add_field(name="Region", value=text[0][3])
            e.add_field(name="Champion", value=text[0][4])
            e.add_field(name="KDA", value=f"{text[0][5]} ({text[0][6]})")
            e.add_field(name="Kill Spree", value=text[0][7])
            e.add_field(name="Damage", value=text[0][8])
            e.add_field(name="Credits", value=text[0][9])
            e.add_field(name="Score", value=text[0][10])
            e.set_author(name=f"Paladins: showing last match", icon_url="https://vignette.wikia.nocookie.net/steamtradingcards/images/7/7d/Paladins_Badge_1.png/revision/latest/top-crop/width/300/height/300?cb=20161215201250")
            e.set_footer(text="Data provided by nonsocial.herokuapp.com")
            #await ctx.send(embed=e)
            await ctx.send(avatar)
            await ctx.send(avatarurl)
            
    @commands.command()
    async def stalk(self, ctx, player, platform="pc"):
        """Shows online/offline status of ``player``"""
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
            e.set_author(name=f"Paladins: showing online/offline status", icon_url="https://vignette.wikia.nocookie.net/steamtradingcards/images/7/7d/Paladins_Badge_1.png/revision/latest/top-crop/width/300/height/300?cb=20161215201250")
            e.set_footer(text="Data provided by nonsocial.herokuapp.com")
            await ctx.send(embed=e)
            
    @commands.command()
    async def current(self, ctx, player, platform="pc"):
        """Shows players in current match and their rank"""
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
            e.set_author(name=f"Paladins: showing current match", icon_url="https://vignette.wikia.nocookie.net/steamtradingcards/images/7/7d/Paladins_Badge_1.png/revision/latest/top-crop/width/300/height/300?cb=20161215201250")
            e.set_footer(text="Data provided by nonsocial.herokuapp.com")
            await ctx.send(embed=e)
            
    @commands.command()
    async def rank(self, ctx, player, platform="pc"):
        """Shows ``player`` rank and ranked k/d/a"""
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
            e.set_author(name=f"Paladins: showing ranked k/d/a", icon_url="https://vignette.wikia.nocookie.net/steamtradingcards/images/7/7d/Paladins_Badge_1.png/revision/latest/top-crop/width/300/height/300?cb=20161215201250")
            e.set_footer(text="Data provided by nonsocial.herokuapp.com")
            await ctx.send(embed=e)
            
    @commands.command()
    async def kda(self, ctx, player, champion="", platform="pc"):
        """Shows ``player`` casual k/d/a"""
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
            e.set_author(name=f"Paladins: showing casual k/d/a", icon_url="https://vignette.wikia.nocookie.net/steamtradingcards/images/7/7d/Paladins_Badge_1.png/revision/latest/top-crop/width/300/height/300?cb=20161215201250")
            e.set_footer(text="Data provided by nonsocial.herokuapp.com")
            await ctx.send(embed=e)
            