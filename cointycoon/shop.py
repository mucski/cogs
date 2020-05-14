import discord
from redbot.core import commands, checks
from .randomstuff import petlist, shoplist

class Shop(commands.Cog):
    #list pets
    @commands.group()
    async def shop(self, ctx):
        pass
    
    @shop.command()
    async def pets(self, ctx):
        """Buy a pet from the list with [p]pet buy petname"""
        imgurl = "https://previews.123rf.com/images/aleksandrax/aleksandrax1704/aleksandrax170400024/76191652-logo-for-pet-shop-veterinary-clinic-animal-shelter-designed-in-a-modern-style-vector-lines-.jpg"
        e = discord.Embed(color=await self.bot.get_embed_color(ctx))
        e.set_author(name="Pet shop", icon_url=imgurl)
        e.set_thumbnail(url=imgurl)
        e.set_footer(text="Buy and own a pet from the above list with .pet buy petname")
        for k, v in petlist.items():
            #build embed
            e.add_field(name=k.capitalize(), value=v['emoji'])
            e.add_field(name="Description", value=v['description'])
            e.add_field(name="Price", value=v['price'])
        await ctx.send(embed=e)
            
    @shop.command()
    async def items(self, ctx):
        """Items"""
        e = discord.Embed()
        e.set_author(name="Item shop", icon_url="")
        e.set_footer(text="Buy an item by typing .shop buy itemname")
        for k, v in shoplist.items():
            #build embed
            e.add_field(name=k.capitalize(), value=v['emoji'])
            e.add_field(name="Description", value=v['description'])
            e.add_field(name="Price", value=v['price'])
            e.add_field(name="Type", value=v['type'])
            e.add_field(name="Quantity/Price", value=v['quantity'])
        await ctx.send(embed=e)
        
    @shop.command()
    async def buyitem(self, ctx, itemname: str, amt: int):
        async with self.conf.user(ctx.author).items() as item:
            item['type'] = shoplist[itemname]['type']
            item['name'] = itemname.capitalize()
            item['quantity'] = amt
            coin = await self.conf.user(ctx.author).coins()
            coins = shoplist[itemname]['price'] * amt
            coin - coins 
            await self.conf.user(ctx.author).coins.set(coin)
            await ctx.send("You bought {} {} for {}".format(item['name'], amt, coins))
            
    @shop.command()
    async def inv(self, ctx):
        items = await self.conf.user(ctx.author).items()
        await ctx.send(items)