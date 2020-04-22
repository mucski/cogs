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
from redbot.core.utils.predicates import MessagePredicate

class Mucski2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #self.conf = Config.get_conf(self, 282828485, forceRegistration=True)
        self.locations = {
            "sewer" : ["You search the sewers for cookies. Imagine finding any.. "],
            "pantry" : ["You search the pantry. Natural birth place of cookies. "],
            "garage" : ["You search the garage for cookies. Look under the car too. "],
            "closet" : ["You search the closet for cookies. Maybe in the pockets of your old clothes. "],
            "cellar" : ["You search the cellar. Odd place to search, but okay, you do you. "],
            "bin" : ["Really? Well you know it. "],
        }
        
    @commands.command()
    async def hello(self, ctx):
        msg = await ctx.send("Hi, what do you want?!")
        predicate = MessagePredicate.same_context(ctx)
        try:        
            m = await ctx.bot.wait_for('message', timeout=60, check=predicate)
        except asyncio.TimeoutError:
            return
        poop = f"you said {m.content}"
        await msg.edit(content=poop)
        await msg.add_reaction('\U0001F39F')
        return
    
    @commands.command()
    async def who(self, ctx, channel: discord.TextChannel, messageid: int):
        try:
            msg = await channel.get_message(messageid)
        except AttributeError:
            try:
                msg = await channel.fetch_message(messageid)
            except discord.HTTPException:
                return await ctx.send("Invalid message id.")
        except discord.HTTPException:
            return await ctx.send("Invalid message id.")
        finally:
            reaction = next(filter(lambda x: x.emoji == '\U0001F39F', msg.reactions), None)
            if reaction is None:
                return await channel.send("no one")
            users = [user for user in await reaction.users().flatten() if ctx.guild.get_member(user.id)]
            await ctx.send(users)
        
    @commands.command()
    async def oof(self, ctx):
        msg = "https://media2.giphy.com/media/S3Qafn57JDnsfRfbFc/giphy.gif"
        e = discord.Embed()
        e.set_image(url=msg)
        await ctx.send(embed=e)
        
    @commands.command()
    async def search(self, ctx):
        location = random.choice(self.locations[1])
        await ctx.send(location[1])
    