import arez
from PIL import ImageOps, ImageDraw, Image, ImageFont
from redbot.core import commands
import asyncio
import aiohttp
import io
import humanize
from datetime import datetime
import discord
from discord import File


class Paladins(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.f = open("/home/ubuntu/key.txt", "r")
        self.auth = self.f.readline()
        self.devid = self.f.readline()
        self.api = arez.PaladinsAPI(dev_id=self.devid.strip(),
                                    auth_key=self.auth.strip())

    def cog_unload(self):
        asyncio.createTask(self.api.close())
        self.f.close()

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            exc = error.original
            if isinstance(exc, arez.Unavailable):
                await ctx.send("HiRez API is offline or unavaiable.")
                return
            if isinstance(exc, arez.Private):
                await ctx.send("Requested profile is set to private")
                return
            if isinstance(exc, arez.NotFound):
                await ctx.send("Player was not found")
                return
        await ctx.bot.on_command_error(ctx, error, unhandled_by_cog=True)

    async def get_champ_image(self, champ):
        champ = champ.lower()
        if "bomb" in champ:
            champ = "bomb-king"
        if "sha" in champ:
            champ = "sha-lin"
        if "mal" in champ:
            champ = "maldamba"
        url = "https://web2.hirez.com/paladins/champion-icons/" \
            + str(champ) + ".jpg"
        return url


    async def stats_image(self, champ_icon, champ_stats, index, party):
        shrink = 140
        offset = 10
        image_size_y = 512 - shrink * 2
        img_x = 512
        middle = image_size_y/2 - 50
        im_color = (175, 238, 238, 0) if index % 2 == 0 else (196, 242, 242, 0)
        img = Image.new("RGBA", (img_x*9, image_size_y+offset*2), color=im_color)
        champ_url = champ_icon
        sessions = aiohttp.ClientSession()
        async with sessions.get(champ_url) as response:
            resp = await response.read()
            champ_icon = Image.open(io.BytesIO(resp))
        sessions.close()
        img.paste(champ_icon, (offset, offset))
        draw = ImageDraw.Draw(img)
        fnt80 = ImageFont.truetype("home/ubuntu/arial.ttf", 80)
        fnt100 = ImageFont.truetype("home/ubuntu/arial.ttf", 100)
        fill = (0, 0, 0)
        # Champion name, player name
        draw.text((img_x+20, middle-40), str(champ_stats[0]), font=fnt80, fill=fill)
        draw.text((img_x+20, middle+60), str(champ_stats[1]), font=fnt80, fill=fill)
        # Parties
        draw.text((img_x+750, middle), champ_stats[2], font=fnt100, fill=fill)
        # Credits
        draw.text((img_x+900, middle), champ_stats[3], font=fnt100, fill=fill)
        # KDA
        draw.text((img_x+1300, middle), champ_stats[4], font=fnt100, fill=fill)
        # Damage Done
        draw.text((img_x+1830, middle), champ_stats[5], font=fnt100, fill=fill)
        # Mitigated
        draw.text((img_x+2350, middle), champ_stats[6], font=fnt100, fill=fill)
        # OBJ time
        draw.text((img_x+2850, middle), champ_stats[7], font=fnt100, fill=fill)
        # Shielding
        draw.text((img_x+3150, middle), champ_stats[8], font=fnt100, fill=fill)
        # Healing
        draw.text((img_x+3600, middle), champ_stats[9], font=fnt100, fill=fill)
        return img


    async def player_key_image(self, x, y):
        key = Image.new("RGBA", (x*9, y-100), color=(112, 225, 255))
        base_draw = ImageDraw.Draw(key)
        fnt80 = ImageFont.truetype("home/ubuntu/arial.ttf", 80)
        # fnt100 = ImageFont.truetype("home/ubuntu/arial.ttf", 100)
        # ss = "Player Credits K/D/A  Damage  Taken  Objective Time  Shielding  Healing"
        base_draw.text((20, 0), "Champion", font=fnt80, fill=(0, 0, 0))
        base_draw.text((x + 20, 0), "Player", font=fnt80, fill=(0, 0, 0))
        # Parties
        fill = (128, 0, 128) if color else (0, 0, 0)
        base_draw.text((x + 750, 0), "P", font=fnt80, fill=fill)
        # Credits/Gold earned
        fill = (218, 165, 32) if color else (0, 0, 0)
        base_draw.text((x + 900, 0), "Credits", font=fnt80, fill=fill)
        # KDA
        fill = (101, 33, 67) if color else (0, 0, 0)
        base_draw.text((x + 1300, 0), "K/D/A", font=fnt80, fill=fill)
        # Damage done
        fill = (255, 0, 0) if color else (0, 0, 0)
        base_draw.text((x + 1830, 0), "Damage", font=fnt80, fill=fill)
        # Damage taken
        fill = (220, 20, 60) if color else (0, 0, 0)
        base_draw.text((x + 2350, 0), "Taken", font=fnt80, fill=fill)
        # Objective time
        fill = (159, 105, 52) if color else (0, 0, 0)
        base_draw.text((x + 2800, 0), "Objective", font=fnt80, fill=fill)
        base_draw.text((x + 2850, 60), "Time", font=fnt80, fill=fill)
        # Shielding
        fill = (0, 51, 102) if color else (0, 0, 0)
        base_draw.text((x + 3150, 0), "Shielding", font=fnt80, fill=fill)
        # Healing
        fill = (0, 128, 0) if color else (0, 0, 0)
        base_draw.text((x + 3600, 0), "Healing", font=fnt80, fill=fill)

        return key

    # Creates a match image based on the two teams champions
    async def history_image(self, team1, team2, t1_data, t2_data, p1, p2, match_data):
        shrink = 140
        image_size_y = 512 - shrink*2
        image_size_x = 512
        offset = 5
        history_image = Image.new('RGB', (image_size_x*9, image_size_y*12 + 264))
        # Adds the top key panel
        key = await self.player_key_image(image_size_x, image_size_y)
        history_image.paste(key, (0, 0))
        # Creates middle panel
        mid_panel = await self.middle_panel(match_data)
        history_image.paste(mid_panel, (0, 1392-40))
        # Adding in player data
        for i, (champ, champ2) in enumerate(zip(team1, team2)):
            try:
                sessions = aiohttp.ClientSession()
                async with sessions.get(champ) as response:
                    resp = await response.read()
                    champ_image = Image.open(io.BytesIO(resp))
                sessions.close()
            except FileNotFoundError:
                champ_image = Image.open("icons/temp_card_art.png")
            border = (0, shrink, 0, shrink)  # left, up, right, bottom
            champ_image = ImageOps.crop(champ_image, border)
            # history_image.paste(champ_image, (0, image_size*i, image_size, image_size*(i+1)))
            player_panel = await create_player_stats_image(champ_image, t1_data[i], i, p1, colored)
            history_image.paste(player_panel, (0, (image_size_y+10)*i+132))
            # Second team
            try:
                sessions = aiohttp.ClientSession()
                async with sessions.get(champ2) as response:
                    resp = await response.read()
                    champ_image = Image.open(io.BytesIO(resp))
                sessions.close()
            except FileNotFoundError:
                champ_image = Image.open("icons/temp_card_art.png")
            border = (0, shrink, 0, shrink)  # left, up, right, bottom
            champ_image = ImageOps.crop(champ_image, border)

            player_panel = await self.stats_image(champ_image, t2_data[i], i+offset-1, p2, colored)
            history_image.paste(player_panel, (0, image_size_y * (i+offset) + 704))
        # Base speed is 10 - seconds
        history_image = history_image.resize((4608//2, 3048//2), Image.ANTIALIAS)           # 5 seconds
        # history_image = history_image.resize((4608 // 4, 3048 // 4), Image.ANTIALIAS)     # 2.5 secs but bad looking
        # Creates a buffer to store the image in
        final_buffer = BytesIO()
        # Store the pillow image we just created into the buffer with the PNG format
        history_image.save(final_buffer, "png")
        # seek back to the start of the buffer stream
        final_buffer.seek(0)
        return final_buffer


    async def middle_panel(self, md):
        middle_panel = Image.new('RGB', (512*9, 512), color=(217, 247, 247))
        # Adding in map to image
        map_name = map_file_name = (md[3].strip().replace("Ranked ", "").replace(" (TDM)", "").replace(" (Onslaught)", "")
                                    .replace(" (Siege)", "")).replace("Practice ", "")
        if "WIP" in map_name:
            map_file_name = "test_maps"
            map_name = map_name.replace("WIP ", "")
        # Needed to catch weird-unknown map modes
        try:
            match_map = Image.open("home/ubuntu/icons/maps/{}.png".format(map_file_name.lower().replace(" ", "_").replace("'", "")))
        except FileNotFoundError:
            match_map = Image.open("home/ubuntu/icons/maps/test_maps.png")
        match_map = match_map.resize((512*2, 512), Image.ANTIALIAS)
        middle_panel.paste(match_map, (0, 0))
        # Preparing the panel to draw on
        draw_panel = ImageDraw.Draw(middle_panel)
        # Add in match information
        ds = 50  # Down Shift
        rs = 20  # Right Shift
        fnt100 = ImageFont.truetype("home/ubuntu/arial.ttf", 100)
        draw_panel.text((512 * 2 + rs, 0 + ds), str(md[0]), font=fnt100, fill=(0, 0, 0))
        draw_panel.text((512 * 2 + rs, 100 + ds), (str(md[1]) + " minutes"), font=fnt100,
                        fill=(0, 0, 0))
        draw_panel.text((512 * 2 + rs, 200 + ds), str(md[2]), font=fnt100, fill=(0, 0, 0))
        draw_panel.text((512 * 2 + rs, 300 + ds), str(map_name), font=fnt100, fill=(0, 0, 0))
        # Right shift
        rs = 100
        # Team 1
        draw_panel.text((512 * 4 + rs, ds), "Team 1 Score: ", font=fnt100, fill=(0, 0, 0))
        draw_panel.text((512 * 4 + rs * 8, ds), str(md[4]), font=fnt100, fill=(0, 0, 0))
        center = (512/2 - 130/2)
        center2 = (512/2 - 80/2)
        # VS
        draw_panel.text((512 * 5-150, center), "VS", font=fnt100, fill=(0, 0, 0))
        # Team 2
        draw_panel.text((512 * 4 + rs, 372), "Team 2 Score: ", font=fnt100, fill=(0, 0, 0))
        draw_panel.text((512 * 4 + rs * 8, 372), str(md[5]), font=fnt100, fill=(0, 0, 0))
        #  add in banned champs if it's a ranked match
        if md[6] is not None:
            # Ranked bans
            draw_panel.text((512 * 5 + rs * 8, center2), "Bans:", font=fnt100, fill=(0, 0, 0))
            # Team 1 Bans
            try:
                sessions = aiohttp.ClientSession()
                async with sessions.get(md[6]) as response:
                    resp = await response.read()
                    champ_icon = Image.open(io.BytesIO(resp))
                sessions.close()
                champ_icon = champ_icon.resize((200, 200))
                middle_panel.paste(champ_icon, (512 * 7 + rs, ds))
            except FileNotFoundError:
                pass

            try:
                sessions = aiohttp.ClientSession()
                async with sessions.get(md[6]) as response:
                    resp = await response.read()
                    champ_icon = Image.open(io.BytesIO(resp))
                sessions.close()
                champ_icon = champ_icon.resize((200, 200))
                middle_panel.paste(champ_icon, (512 * 7 + rs + 240, ds))
            except FileNotFoundError:
                pass
            # Team 2 Bans
            try:
                sessions = aiohttp.ClientSession()
                async with sessions.get(md[6]) as response:
                    resp = await response.read()
                    champ_icon = Image.open(io.BytesIO(resp))
                sessions.close()
                champ_icon = champ_icon.resize((200, 200))
                middle_panel.paste(champ_icon, (512 * 7 + rs, ds+232))
            except FileNotFoundError:
                pass
            try:
                sessions = aiohttp.ClientSession()
                async with sessions.get(md[6]) as response:
                    resp = await response.read()
                    champ_icon = Image.open(io.BytesIO(resp))
                sessions.close()
                champ_icon = champ_icon.resize((200, 200))
                middle_panel.paste(champ_icon, (512 * 7 + rs + 240, ds+232))
            except FileNotFoundError:
                pass

        return middle_panel


    @commands.command()
    async def hitest(self, ctx, matchId):
        match = await self.api.get_match(matchId, expand_players=True)
        team1_data = []
        team2_data = []
        team1_champs = []
        team2_champs = []
        team1_parties = {}
        team2_parties = {}
        temp = []
        new_party_id = 0
        if matchId == -1 or matchId == match.id:
            # match_data = self.bot.paladinsAPI.getMatch(match.matchId)
            match_info = [match.winning_team, match.duration, match.region,
                          match.map_name, match.score[0], match.score[1]]
            temp = match.bans
        for player in match.team1:
            kda = match.team1.player.kda_text
            team1_data.append([match.team1.player, match.team1.player.account_level, match.team1.player.credits, kda,
                               match.team1.player.damage_done, match.team1.player.damage_taken,
                               match.team1.player.objective_time, match.team1.player.damage_mitigated,
                               match.team1.player.healing_done, match.team1.player.party_number, match.team1.player.platform])
            team1_champs.append(match.team1.player.champion)
            if match.team1.player.party_number not in team1_parties or match.team1.player.party_number == 0:
                team1_parties[match.team1.player.party_number] = ""
            else:
                if team1_parties[match.team1.player.party_number] == "":
                    new_party_id += 1
                    team1_parties[match.team1.player.party_number] = "" + str(new_party_id)
        for player in match.team2:
            kda = match.team2.player.kda_text
            team2_data.append([match.team2.player.player, match.team2.player.account_level, match.team2.player.credits, kda,
                               match.team2.player.damage_done, match.team2.player.damage_taken,
                               match.team2.player.objective_time, match.team2.player.damage_mitigated,
                               match.team2.player.healing_done, match.team2.player.party_number, match.team2.player.platform])
            team2_champs.append(match.team2.player.champion)
            if match.team2.player.party_number not in team1_parties or match.team2.player.party_number == 0:
                team1_parties[match.team2.player.party_number] = ""
            else:
                if team2_champs[match.team2.player.party_number] == "":
                    new_party_id += 1
                    team2_champs[match.team2.player.party_number] = "" + str(new_party_id)
        buffer = await self.history_image(team1_champs, team2_champs, team1_data, team2_data,
                                                               team1_parties, team2_parties, (match_info + temp))
        file = discord.File(filename="TeamMatch.png", fp=buffer)
        await ctx.send("```You are an amazing person!```", file=file)

    @commands.command()
    async def atest(self, ctx, matchId):
        match = await self.api.get_match(matchId, expand_players=True)
        for players in match.team1:
            player = match.players.player
        await ctx.send(player)

    @commands.command()
    async def stats(self, ctx, player, platform="PC"):
        platform = arez.Platform(platform)
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
            f"Account Created: "
            f"{humanize.naturaltime(datetime.utcnow() - player.created_at)}\n"
            f"Last Login: "
            f"{humanize.naturaltime(datetime.utcnow() - player.last_login)}\n"
            "```\n\n"
            f"**__Casual Stats__**\n"
            f"```Win Rate: "
            f"{player.casual.wins}/{player.casual.losses}"
            f" ({player.casual.winrate_text})\n"
            f"Deserted: {player.casual.leaves}\n```"
            "\n\n"
            f"**__Ranked Stats Season {player.ranked_best.season}__**\n"
            f"```Win Rate: "
            f"{player.ranked_best.wins}/{player.ranked_best.losses}"
            f" ({player.ranked_best.winrate_text})\n"
            f"Deserted: {player.ranked_best.leaves}\n"
            f"Ranked Type: {player.ranked_best.type}\n"
            f"Current Rank: {player.ranked_best.rank}"
            f" ({player.ranked_best.points} TP)\n```"
        )
        e = discord.Embed(color=await self.bot.get_embed_color(ctx),
                          title=f"{player.name}({player.platform})"
                                f"_({player.title})_")
        e.description = desc
        e.set_thumbnail(url=player.avatar_url)
        e.set_footer(text=f"Player ID: {player.id}")
        await ctx.send(embed=e)
