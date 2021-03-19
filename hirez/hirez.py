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
from PIL import Image, ImageFont, ImageDraw, ImageOps

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
            #elif isinstance(exc, IndexError):
            #    await ctx.send("Player did not play for over a month, therefore nothing to display.")
            #    return
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

    async def match_history_image(self, team1, team2, t1_data, t2_data, party1, party2, match_data):
        shrink = 140
        image_size_y = 540 - shrink*2
        image_size_x = 540
        offset = 5
        history_image = Image.new('RGB', (image_size_x*9, image_size_y*12 + 264))
        #top key panel
        key = await self.player_key_image(image_size_x, image_size_y)
        history_image.paste(key, (0, 0))
        #create middle panel
        mid_panel = await self.middle_info_image(match_data)
        history_image.paste(mid_panel, (0, 1392-40))
        #player data
        for i, (champ, champ2) in enumerate(zip(team1, team2)):
            #first team
            try:
                champ_url = await self.get_champ_image(champ)
                sessions = aiohttp.ClientSession()
                async with sessions.get(champ_url) as response:
                    resp = await response.read()
                    champ_image = Image.open(BytesIO(resp))
                sessions.close()
            except FileNotFoundError:
                champ_image = Image.open("/home/ubuntu/icons/temp_card_art.png")
            border = (0, shrink, 0, shrink) #left, up, right, bottom
            champ_image = ImageOps.crop(champ_image, border)
            player_panel = await self.player_stats_image(champ_image, t1_data[i], i, party1)
            history_image.paste(player_panel, (image_size_y+10)*i+132)

            #second team
            try:
                champ_url = await self.get_champ_image(champ2)
                sessions = aiohttp.ClientSession()
                async with sessions.get(champ_url) as response:
                    resp = await response.read()
                    champ_image = Image.open(BytesIO(resp))
                sessions.close()
            except FileNotFoundError:
                champ_image = Image.open("/home/ubuntu/icons/temp_card_art.png")
            border = (0, shrink, 0, shrink) #left, up, right, bottom
            champ_image = ImageOps.crop(champ_image, border)
            player_panel = await self.player_stats_image(champ_image, t2_data[i], i+offset-1, party2)
            history_image.paste(player_panel, (0, image_size_y * (i+offset) + 704))

        history_image = history_image.resize((4608//2, 3048//2), Image.ANTIALIAS)

        final_buffer = BytesIO()

        history_image.save(final_buffer, "png")

        final_buffer.seek(0)

        return final_buffer

    async def middle_info_image(self, match_data):
        font = "/home/ubuntu/arial.ttf"
        middle_panel = Image.new('RGB', (512*9, 512), color=(217, 247, 247))

        # Adding in map to image
        map_name = map_file_name = (match_data[3].strip().replace("Ranked ", "").replace(" (TDM)", "").replace(" (Onslaught)", "")
                                .replace(" (Siege)", "")).replace("Practice ", "")
        if "WIP" in map_name:
            map_file_name = "test_maps"
            map_name = map_name.replace("WIP ", "")
        # Needed to catch weird-unknown map modes
        try:
            match_map = Image.open("/home/ubuntu/icons/maps/{}.png".format(map_file_name.lower().replace(" ", "_").replace("'", "")))
        except FileNotFoundError:
            match_map = Image.open("/home/ubuntu/icons/maps/test_maps.png")   
        match_map = match_map.resize((512*2, 512), Image.ANTIALIAS)
        middle_panel.paste(match_map, (0, 0))
        # Preparing the panel to draw on
        draw_panel = ImageDraw.Draw(middle_panel)
        # Add in match information
        ds = 50  # Down Shift
        rs = 20  # Right Shift
        draw_panel.text((512 * 2 + rs, 0 + ds), str(match_data[0]), font=ImageFont.truetype(font, 100), fill=(0, 0, 0))
        draw_panel.text((512 * 2 + rs, 100 + ds), (str(match_data[1]) + " minutes"), font=ImageFont.truetype(font, 100),
                        fill=(0, 0, 0))
        draw_panel.text((512 * 2 + rs, 200 + ds), str(match_data[2]), font=ImageFont.truetype(font, 100), fill=(0, 0, 0))
        draw_panel.text((512 * 2 + rs, 300 + ds), str(map_name), font=ImageFont.truetype(font, 100), fill=(0, 0, 0))

        # Right shift
        rs = 100
        # Team 1
        draw_panel.text((512 * 4 + rs, ds), "Team 1 Score: ", font=ImageFont.truetype(font, 100), fill=(0, 0, 0))
        draw_panel.text((512 * 4 + rs * 8, ds), str(match_data[4]), font=ImageFont.truetype(font, 100), fill=(0, 0, 0))

        center = (512/2 - 130/2)
        center2 = (512/2 - 80/2)
        # VS
        draw_panel.text((512 * 5-150, center), "VS", font=ImageFont.truetype(font, 130), fill=(0, 0, 0))

        # Team 2
        draw_panel.text((512 * 4 + rs, 372), "Team 2 Score: ", font=ImageFont.truetype(font, 100), fill=(0, 0, 0))
        draw_panel.text((512 * 4 + rs * 8, 372), str(match_data[5]), font=ImageFont.truetype(font, 100), fill=(0, 0, 0))

        #  add in banned champs if it's a ranked match
        if match_data[6] is not None:
            # Ranked bans
            draw_panel.text((512 * 5 + rs * 8, center2), "Bans:", font=ImageFont.truetype(font, 80), fill=(0, 0, 0))

            # Team 1 Bans
            try:
                champ_url = await self.get_champ_image(match_data[6])
                sessions = aiohttp.ClientSession()
                async with sessions.get(champ_url) as response:
                    resp = await response.read()
                    champ_image = Image.open(BytesIO(resp))
                sessions.close()
                champ_image = champ_image.resize((200, 200))
                middle_panel.paste(champ_image, (512 * 7 + rs, ds))
            except FileNotFoundError:
                pass

            try:
                champ_url = await self.get_champ_image(match_data[7])
                sessions = aiohttp.ClientSession()
                async with sessions.get(champ_url) as response:
                    resp = await response.read()
                    champ_image = Image.open(BytesIO(resp))
                sessions.close()
                champ_image = champ_image.resize((200, 200))
                middle_panel.paste(champ_image, (512 * 7 + rs + 240, ds))
            except FileNotFoundError:
                pass

            # Team 2 Bans
            try:
                champ_url = await self.get_champ_image(match_data[8])
                sessions = aiohttp.ClientSession()
                async with sessions.get(champ_url) as response:
                    resp = await response.read()
                    champ_image = Image.open(BytesIO(resp))
                sessions.close()
                champ_image = champ_image.resize((200, 200))
                middle_panel.paste(champ_image, (512 * 7 + rs, ds+232))
            except FileNotFoundError:
                pass

            try:
                champ_url = await self.get_champ_image(match_data[9])
                sessions = aiohttp.ClientSession()
                async with sessions.get(champ_url) as response:
                    resp = await response.read()
                    champ_image = Image.open(BytesIO(resp))
                sessions.close()
                champ_image = champ_image.resize((200, 200))
                middle_panel.paste(champ_image, (512 * 7 + rs + 240, ds+232))
            except FileNotFoundError:
                pass

        return middle_panel

    async def player_stats_image(self, champ_icon, champ_stats, index, party):
        font = "/home/ubuntu/arial.ttf"
        shrink = 140
        offset = 10
        image_size_y = 512 - shrink * 2
        img_x = 512
        middle = image_size_y/2 - 50
        im_color = (175, 238, 238, 0) if index % 2 == 0 else (196, 242, 242, 0)
        # color = (175, 238, 238)   # light blue
        # color = (196, 242, 242)     # lighter blue
        champ_stats_image = Image.new('RGBA', (img_x*9, image_size_y+offset*2), color=im_color)

        champ_stats_image.paste(champ_icon, (offset, offset))

        platform = champ_stats[11]
        if platform == "XboxLive":
            platform_logo = Image.open("/home/ubuntu/icons/xbox_logo.png").resize((100, 100), Image.ANTIALIAS)
            platform_logo = platform_logo.convert("RGBA")
            champ_stats_image.paste(platform_logo, (img_x + 175, int(middle) + 60), platform_logo)
        elif platform == "Nintendo Switch":
            platform_logo = Image.open("/home/ubuntu/icons/switch_logo.png")
            width, height = platform_logo.size
            scale = .15
            platform_logo = platform_logo.resize((int(width * scale), int(height * scale)), Image.ANTIALIAS)
            platform_logo = platform_logo.convert("RGBA")
            champ_stats_image.paste(platform_logo, (img_x + 135, int(middle) + 45), platform_logo)
        elif platform == "PSN":
            platform_logo = Image.open("/home/ubuntu/icons/ps4_logo.png").resize((100, 100), Image.ANTIALIAS)
            platform_logo = platform_logo.convert("RGBA")
            champ_stats_image.paste(platform_logo, (img_x + 175, int(middle) + 60), platform_logo)
        # For future if I want to add a PC icon
        # else:
        #    print("PC")

        # if platform_logo:
        #    platform_logo = platform_logo.convert("RGBA")
        #    champ_stats_image.paste(platform_logo, (img_x + 175, int(middle)+60), platform_logo)
        #    # champ_stats_image.show()

        base_draw = ImageDraw.Draw(champ_stats_image)

        # Private account or unknown
        if str(champ_stats[0]) == "":
            champ_stats[0] = "*****"

        # Player name and champion name
        base_draw.text((img_x + 20, middle-40), str(champ_stats[0]), font=ImageFont.truetype(font, 80), fill=(0, 0, 0))
        base_draw.text((img_x + 20, middle+60), str(champ_stats[1]), font=ImageFont.truetype(font, 80), fill=(0, 0, 0))

        # Parties
        fill = (128, 0, 128)
        base_draw.text((img_x + 750, middle), party[champ_stats[3]], font=ImageFont.truetype(font, 100), fill=fill)

        # Credits/Gold earned
        fill = (218, 165, 32)
        base_draw.text((img_x + 900, middle), str(champ_stats[4]), font=ImageFont.truetype(font, 100), fill=fill)

        # KDA
        fill = (101, 33, 67)
        base_draw.text((img_x + 1300, middle), str(champ_stats[5]), font=ImageFont.truetype(font, 100), fill=fill)

        # Damage done
        fill = (255, 0, 0)
        base_draw.text((img_x + 1830, middle), str(champ_stats[6]), font=ImageFont.truetype(font, 100), fill=fill)

        # Damage taken
        fill = (220, 20, 60)
        base_draw.text((img_x + 2350, middle), str(champ_stats[7]), font=ImageFont.truetype(font, 100), fill=fill)

        # Objective time
        fill = (159, 105, 52)
        base_draw.text((img_x + 2850, middle), str(champ_stats[8]), font=ImageFont.truetype(font, 100), fill=fill)

        # Shielding
        fill = (0, 51, 102)
        base_draw.text((img_x + 3150, middle), str(champ_stats[9]), font=ImageFont.truetype(font, 100), fill=fill)

        # Healing
        fill = (0, 128, 0)
        base_draw.text((img_x + 3600, middle), str(champ_stats[10]), font=ImageFont.truetype(font, 100), fill=fill)

        return champ_stats_image

    # Creates the text at the top of the image
    async def player_key_image(self, x, y):
        font = "/home/ubuntu/arial.ttf"
        key = Image.new('RGB', (x * 9, y-100), color=(112, 225, 225))
        base_draw = ImageDraw.Draw(key)
        # ss = "Player Credits K/D/A  Damage  Taken  Objective Time  Shielding  Healing"
        base_draw.text((20, 0), "Champion", font=ImageFont.truetype(font, 80), fill=(0, 0, 0))
        base_draw.text((x + 20, 0), "Player", font=ImageFont.truetype(font, 80), fill=(0, 0, 0))

        # Parties
        fill = (128, 0, 128) 
        base_draw.text((x + 750, 0), "P", font=ImageFont.truetype(font, 100), fill=fill)

        # Credits/Gold earned
        fill = (218, 165, 32) 
        base_draw.text((x + 900, 0), "Credits", font=ImageFont.truetype(font, 80), fill=fill)

        # KDA
        fill = (101, 33, 67) 
        base_draw.text((x + 1300, 0), "K/D/A", font=ImageFont.truetype(font, 80), fill=fill)

        # Damage done
        fill = (255, 0, 0) 
        base_draw.text((x + 1830, 0), "Damage", font=ImageFont.truetype(font, 80), fill=fill)

        # Damage taken
        fill = (220, 20, 60) 
        base_draw.text((x + 2350, 0), "Taken", font=ImageFont.truetype(font, 80), fill=fill)

        # Objective time
        fill = (159, 105, 52) 
        base_draw.text((x + 2800, 0), "Objective", font=ImageFont.truetype(font, 60), fill=fill)
        base_draw.text((x + 2850, 60), "Time", font=ImageFont.truetype(font, 60), fill=fill)

        # Shielding
        fill = (0, 51, 102) 
        base_draw.text((x + 3150, 0), "Shielding", font=ImageFont.truetype(font, 80), fill=fill)

        # Healing
        fill = (0, 128, 0) 
        base_draw.text((x + 3600, 0), "Healing", font=ImageFont.truetype(font, 80), fill=fill)

        return key

    @commands.command()
    async def atest(self, ctx):
        match_data = ["TEAM 1", "32", "Europe", "Timber Mill", "4/1"]
        bans = ["Sha Lin, Ruckus", "Tiberius", "Raum"]
        await ctx.send(match_data + bans)

    @commands.command()
    async def hitest(self, ctx):
        team1 = ["Makoa", "Cassie", "Strix", "Bomb King", "IO"]
        team2 = ["Atlas", "Vora", "Yagorath", "Jenos", "Dredge"]
        t1_data = []
        t2_data = []
        party1 = ["0","0","0","0","0"]
        party2 = ["0","0","0","0","0"]
        match_data = ["1", "32", "Europe", "Timber Mill", "4", "1"]
        bans = ["Sha Lin, Ruckus", "Tiberius", "Raum"]
        #player name, champion, party, credit, kda, damage, damage taken, obj time, shielding, healing
        t1 = ["Joey", "999", "0", "3409", "24/1/93", "83834", "34849", "143", "382834", "338423", "PC"]
        t2 = ["Joey", "999", "0", "3409", "24/1/93", "83834", "34849", "143", "382834", "338423", "PC"]
        t3 = ["Joey", "999", "0", "3409", "24/1/93", "83834", "34849", "143", "382834", "338423", "PC"]
        t4 = ["Joey", "999", "0", "3409", "24/1/93", "83834", "34849", "143", "382834", "338423", "PC"]
        t5 = ["Joey", "999", "0", "3409", "24/1/93", "83834", "34849", "143", "382834", "338423", "PC"]
        t1_data.append([t1, t2, t3, t4, t5])
        t2_data.append([t1, t2, t3, t4, t5])
        #final_buffer = await self.match_history_image(team1, team2, t1_data, t2_data, party1, party2, (match_info + bans))
        final_buffer = await self.match_history_image(team1, team2, t1_data, t2_data, party1, party2, (match_data + bans))
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