import arez
import discord
import asyncio
import humanize
import time
import aiohttp
from datetime import datetime
from redbot.core import commands
from tabulate import tabulate
from redbot.core.utils.chat_formatting import pagify
from redbot.core.utils.chat_formatting import box
import discord
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw

class  Hirez(commands.Cog):
    """
    Returns stats for Paladins made by Evil Mojo Studios
    Every command is subject to change and in constant development.
    Version: 0.1.24

    Developed by Mucski
    """
    def __init__(self, bot):
        self.bot = bot
        self.f = open("/home/ubuntu/key.txt", "r")
        self.auth = self.f.readline()
        self.devid = self.f.readline()
        self.api = arez.PaladinsAPI(dev_id=self.devid.strip(), auth_key=self.auth.strip())
       
    def cog_unload(self):
        asyncio.create_task(self.api.close())
        self.f.close()

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            exc = error.original
            if isinstance(exc, arez.Unavailable):
                await ctx.send("Hi-Rez API currently shat itself. Offline or unavailable.")
                return
            elif isinstance(exc, arez.Private):
                await ctx.send("The requested users profile is set to private.")
                return
            elif isinstance(exc, arez.NotFound):
                await ctx.send("Player was not found.")
                return
            elif isinstance(exc, IndexError):
                await ctx.send("Player did not play for over a month, therefore nothing to display.")
                return
            # elif isinstance(exc, ...):
            #     await ctx.send(...)
            #     return
        await ctx.bot.on_command_error(ctx, error, unhandled_by_cog=True)

    async def get_champ_image(self, champ_name):
        champ_name = champ_name.lower()
        if "bomb" in champ_name:
            champ_name = "bomb-king"
        if "mal" in champ_name:
            champ_name = "maldamba"
        if "sha" in champ_name:
            champ_name = "sha-lin"
        #just return the champ_name as it is
        url = "https://web2.hirez.com/paladins/champion-icons/" + str(champ_name) + ".jpg"
        return url

    async def create_team_image(self, champ_list, ranks):
        font = "/home/ubuntu/arial.ttf"
        champion_images = []

        while len(champ_list) != 5:
            champ_list.append("?")
        
        for champ in champ_list:
            if champ != "?":
                champ_url = await self.get_champ_image(champ)
                sessions = aiohttp.ClientSession()
                response = sessions.get(champ_url)
                champion_images.append(Image.open(BytesIO(response.content)))
                sessions.close()
            else:
                image_size = 512
                base = Image.new('RGB', (image_size, image_size), black)

                #put text on image
                base_draw = ImageDraw.Draw(base)
                base_draw.text((128, 56), "?", font=ImageFont.truetype(font, 400))
                champion_images.append(base)

        #image size in width height
        image_size = 512
        scale = 1.5

        team_image = Image.new('RGB', (image_size * len(champion_images), image_size))
        for i, champ in enumerate(champion_images):
            team_image.paste(champ, (image_size*i, 0, image_size*(i+1), image_size))

            #only use ranked image if its a ranked match.
            if ranks:
                if i < len(ranks):  # make sure we don't go out of bounds
                    rank = Image.open("/home/ubuntu/icons/ranks/" + ranks[i] + ".png")  # this works
                    width, height = rank.size
                    rank = rank.resize((int(width * scale), int(height * scale)))
                    team_image.paste(rank, (0 + (image_size * i), 0), rank)  # Upper Left

        # Creates a buffer to store the image in
        final_buffer = BytesIO()

        # Store the pillow image we just created into the buffer with the PNG format
        team_image.save(final_buffer, "png")

        # seek back to the start of the buffer stream
        final_buffer.seek(0)

        return final_buffer

    @commands.command()
    async def hitest(self, ctx):
        sex = ["bomb", "sha", "strix", "kinessa", "vora"]
        ranks = ["gold", "gold", "silver", "bronze", "bronze"]
        final_buffer = await self.create_team_image(sex, ranks)
        file = discord.File(filename="TeamMatch.png", fp=final_buffer)
        await ctx.send(file=file)

    @commands.command()
    async def stats(self, ctx, player, platform="pc"):
        """Player stats, title, avatar and more"""
        start_time = time.time()
        platform = arez.Platform(platform)
        if platform is None:
            await ctx.send("Wrong platform buster!")
            return
        if player.isdecimal():
            player = await self.api.get_player(player)  
        else:
            player_obj = await self.api.search_players(player, platform)
            player = await player_obj[0]
        desc = (
            "**__Player Stats__**\n"
            f"```Account level: {player.level}\n"
            f"Playtime: {int(player.playtime.total_hours())} hours\n"
            f"Region: {player.region}\n"
            f"Champions Owned: {player.champion_count}\n"
            f"Achievements Unlocked: {player.total_achievements}\n"
            f"Account Created: {humanize.naturaltime(datetime.utcnow() - player.created_at)}\n"
            f"Last Login: {humanize.naturaltime(datetime.utcnow() - player.last_login)}\n```"
            "\n\n"
            f"**__Casual Stats__**\n"
            f"```Win Rate: {player.casual.wins} / {player.casual.losses} ({player.casual.winrate_text})\n"
            f"Deserted: {player.casual.leaves}\n```"
            "\n\n"
            f"**__Ranked Stats Season {player.ranked_best.season}__**\n"
            f"```Win Rate: {player.ranked_best.wins} / {player.ranked_best.losses} ({player.ranked_best.winrate_text})\n"
            f"Deserted: {player.ranked_best.leaves}\n"
            f"Ranked Type: {player.ranked_best.type}\n"
            f"Current Rank: {player.ranked_best.rank} ({player.ranked_best.points} TP)\n```"
        )
        embed = discord.Embed(color=await self.bot.get_embed_color(ctx), title=f"{player.name}({player.platform}) _{player.title}_")
        embed.description=desc
        #embed.set_author(name=f"{player.name}({player.platform})")
        embed.set_thumbnail(url=player.avatar_url)
        embed.set_footer(text=f"Fetched in {(time.time() - start_time)}, ID: {player.id}")
        await ctx.send(embed=embed)
        
    @commands.command()
    async def matchimage(self, ctx, player, match_id=None):
        #platform = arez.Platform(platform)

            #buffer = 

            #file = discord.File(filename="TeamMatch.png", fp=buffer)
        #await ctx.send(file=file)
        pass
        
    @commands.command()
    async def match(self, ctx, player, platform="pc"):
        """A match played by a player"""
        platform = arez.Platform(platform)
        if platform is None:
            await ctx.send("Wrong platform buster!")
            return
        if player.isdecimal():
            player = await self.api.get_player(player)
        else:
            player_obj = await self.api.search_players(player, platform)
            player = await player_obj[0]
        history = await player.get_match_history()
        last = history[0]
        match = await self.api.get_match(last.id)
        #Build embed
        e = discord.Embed(color=await self.bot.get_embed_color(ctx), title=f"Detailed match for {player.name}({player.platform})")
        e.add_field(name="Player ID / Player Level", value=f"``{player.id}`` / {player.level}")
        if last.champion is not None:
            e.set_thumbnail(url=last.champion.icon_url)
        else:
            e.set_thumbnail(url=ctx.author.avatar_url)
        e.add_field(name="Match", value=f"``{match.id}`` - {match.queue} - {match.map_name}")
        e.add_field(name="Duration / Region", value=f"{match.duration} / { match.region}")
        e.add_field(name="Score / Winning Team", value=f"{match.score} / ``Team {match.winning_team}``")
        e.add_field(name="Replay Available", value=f"{match.replay_available}")
        if match.bans:
            e.add_field(name="Banned champions:", value='\n'.join(ch.name for ch in match.bans), inline=False)
        else:
            pass
        e.add_field(name="Team 1\nPlayer Name / ID / KDA / Damage / Healing or Shielding", value='\n'.join(map(str, match.team1)).replace(f"{player.name}", f"``{player.name}``"), inline="False")
        e.add_field(name="Team 2\nPlayer Name / ID / KDA / Damage / Healing or Shielding", value='\n'.join(map(str, match.team2)).replace(f"{player.name}", f"``{player.name}``"), inline="False")
        e.set_footer(text=f"Played: {humanize.naturaltime(datetime.utcnow() - match.timestamp)}")
        await ctx.send(embed=e)

    @commands.command()
    async def current(self, ctx, player, platform="pc"):
        """A match played by a player"""
        platform = arez.Platform(platform)
        if platform is None:
            await ctx.send("Wrong platform buster!")
            return
        if player.isdecimal():
            player = await self.api.get_player(player)  
        else:
            player_obj = await self.api.search_players(player, platform)
            player = await player_obj[0]
        status = await player.get_status()
        match =  await status.get_live_match()
        if match is None:
            await ctx.send("Player not in a match")
            return
        e = discord.Embed(color=await self.bot.get_embed_color(ctx), title=f"Current match for {player.name} - _{player.title}_")
        e.set_thumbnail(url=player.avatar_url)
        e.add_field(name="Match", value=f"``{match.id}`` - {match.queue} - {match.map_name} - { match.region}")
        e.add_field(name="Team 1\nPlayer Name / ID / KDA / Damage / Healing or Shielding", value='\n'.join(map(str, match.team1)).replace(f"{player.name}", f"``{player.name}``"), inline="False")
        e.add_field(name="Team 2\nPlayer Name / ID / KDA / Damage / Healing or Shielding", value='\n'.join(map(str, match.team2)).replace(f"{player.name}", f"``{player.name}``"), inline="False")
        await ctx.send(embed=e)        
        
    @commands.command()
    async def history(self, ctx, player, platform = "pc"):
        """Player history"""
        platform = arez.Platform(platform)
        if platform is None:
            await ctx.send("Wrong platform buster!")
            return
        if player.isdecimal():
            player = await self.api.get_player(player)
        else:
            player_obj = await self.api.search_players(player, platform)
            player = await player_obj[0]
        history = await player.get_match_history()
        matches = []
        for match in history: #[:30]
            matchlist = []
            if match.winner == True:
                matchlist.append("+ WON")
                matchlist.append(match)
            else:
                matchlist.append("- LOST")
                matchlist.append(match)
            matches.append(matchlist)
        
        table = tabulate(matches, headers=["# W/L", "QUEUE/CHAMPION/SCORE"])
        lenght = "\n".join(table)
        if len(lenght) < 2000:
            await ctx.send(box(table, lang='diff'))
        else:
            for page in pagify(table):
                await ctx.send(box(page, lang='diff'))
    
    @commands.command()
    async def status(self, ctx):
        status = arez.StatusPage("http://status.hirezstudios.com/")
        csirke = await status.get_status()
        desc = (
            f"**Hirez Infrastructure**: {csirke.status}\n"
            f"**Incident Impact**: {csirke.impact}\n"
            f"**{csirke.component('Paladins PC').name}**: {csirke.component('Paladins PC').status}\n"
            f"**{csirke.component('Paladins PS4').name}**: {csirke.component('Paladins PS4').status}\n"
            f"**{csirke.component('Paladins Xbox').name}**: {csirke.component('Paladins Xbox').status}\n"
            f"**{csirke.component('Paladins Switch').name}**: {csirke.component('Paladins Switch').status}\n"
            f"**{csirke.component('Paladins Epic').name}**: {csirke.component('Paladins Epic').status}\n"
            f"**{csirke.component('Hi-Rez Public APIs').name}**: {csirke.component('Hi-Rez Public APIs').status}\n"
        )
        e = discord.Embed(color=csirke.color, title="Hirez Status", description=desc)
        e.set_footer(text=f"Last updated at: {csirke.updated_at}")
        await ctx.send(embed=e)
    
    @commands.command()
    async def last(self, ctx, player, platform = "pc"):
        start_time = time.time()
        """Player stats from the last match"""
        platform = arez.Platform(platform)
        if platform is None:
            await ctx.send("Wrong platform buster!")
            return
        if player.isdecimal():
            player = await self.api.get_player(player)
        else:
            player_obj = await self.api.search_players(player, platform)
            player = await player_obj[0]
        history = await player.get_match_history()
        last = history[0]
        if last.winner == True:
            winner = "Win"
            color = 0x00ccff
        else:
            winner = "Loss"
            color = 0xee1515
        embed = discord.Embed(color=color, title=f"Match ID: `{last.id}` Played: `{humanize.naturaltime(datetime.utcnow() - last.timestamp)}`")
        embed.set_author(name=f"{player.name}({last.player.platform})")
        if last.champion is not None:
            embed.set_thumbnail(url=last.champion.icon_url)
        else:
            embed.set_thumbnail(url=ctx.author.avatar_url)
        if last.champion is not None:
            champ = last.champion.name
        else:
            champ = 'Unknown'
        items = last.items
        item = '\n'.join(map(str, items))
        cards = '\n'.join(map(str, last.loadout.cards))
 
        embed.description = desc
        embed.set_footer(text=f"Played {humanize.naturaltime(datetime.utcnow() - last.timestamp)}")
        await ctx.send(embed=embed)