from PIL import ImageOps, ImageDraw, Image, ImageFont
import aiohttp
from io import BytesIO
from redbot.core.utils.chat_formatting import humanize_number


class helper:

    @classmethod
    async def get_champ_image(cls, champ):
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

    @classmethod
    async def get_rank_image(cls, rank):
        pass

    @classmethod
    async def stats_image(cls, champ_icon, rank_icon, champ_stats, index):
        shrink = 140
        offset = 10
        image_size_y = 512 - shrink * 2
        img_x = 512
        middle = image_size_y/2 - 50
        im_color = (14, 34, 43) if index % 2 == 0 else (15, 40, 48)
        orange = (252, 186, 3)
        green = (7, 252, 3)
        red = (252, 102, 3)
        purple = (240, 3, 252)
        fill = (255, 255, 255)
        if champ_stats[9] == 1:
            color = green
        elif champ_stats[9] == 2:
            color = orange
        elif champ_stats[9] == 3:
            color = red
        elif champ_stats[9] == 4:
            color = purple
        else:
            color = fill
        img = Image.new(
            "RGBA", (img_x*10, image_size_y+offset*2), color=im_color)
        img.paste(champ_icon, (offset, offset))
        img.paste(rank_icon, (1220, int(middle)), mask=rank_icon)
        draw = ImageDraw.Draw(img)
        fnt80 = ImageFont.truetype("home/ubuntu/arial.ttf", 80)
        fnt100 = ImageFont.truetype("home/ubuntu/arial.ttf", 100)
        fnt80bold = ImageFont.truetype("home/ubuntu/arialbd.ttf", 80)
        if champ_stats[0] == "":
            champ_stats[0] = "???????"
        # Champion name, player name
        draw.text((img_x+20, middle-40),
                  str(champ_stats[0]), font=fnt80bold, fill=color)
        draw.text((img_x+20, middle+60),
                  str(champ_stats[1]), font=fnt80, fill=fill)
        # Rank
        # draw.text((img_x+750, middle), rank_icon, font=fnt100, fill=fill)
        # Parties
        draw.text((img_x+950, middle),
                  str(champ_stats[9]), font=fnt100, fill=fill)
        # Credits
        draw.text((img_x+1100, middle),
                  humanize_number(champ_stats[2]), font=fnt100, fill=fill)
        # KDA
        draw.text((img_x+1500, middle),
                  str(champ_stats[3]), font=fnt100, fill=fill)
        # Damage Done
        draw.text((img_x+1950, middle),
                  humanize_number(champ_stats[4]), font=fnt100, fill=fill)
        # Mitigated
        draw.text((img_x+2450, middle),
                  humanize_number(champ_stats[5]), font=fnt100, fill=fill)
        # OBJ time
        draw.text((img_x+2900, middle),
                  humanize_number(champ_stats[6]), font=fnt100, fill=fill)
        # Shielding
        draw.text((img_x+3250, middle),
                  humanize_number(champ_stats[7]), font=fnt100, fill=fill)
        # Healing
        draw.text((img_x+3750, middle),
                  humanize_number(champ_stats[8]), font=fnt100, fill=fill)
        # Self Healing
        draw.text((img_x+4220, middle),
                  humanize_number(champ_stats[11]), font=fnt100, fill=fill)
        return img

    @classmethod
    async def player_key_image(cls, x, y):
        key = Image.new("RGBA", (x*10, y-100), color=(8, 21, 25))
        base_draw = ImageDraw.Draw(key)
        fill = (255, 255, 255)
        fnt80bold = ImageFont.truetype("home/ubuntu/arialbd.ttf", 80)
        # fnt100 = ImageFont.truetype("home/ubuntu/arial.ttf", 100)
        # ss = "Player Credits K/D/A  Damage  Taken  Objective Time  Shielding  Healing"
        base_draw.text((20, 0), "Champion", font=fnt80bold,
                       fill=(255, 255, 255))
        base_draw.text((x + 20, 0), "Player",
                       font=fnt80bold, fill=(255, 255, 255))
        # Ranks
        base_draw.text((x + 750, 0), "R", font=fnt80bold, fill=fill)
        # Parties
        base_draw.text((x + 950, 0), "P", font=fnt80bold, fill=fill)
        # Credits/Gold earned
        base_draw.text((x + 1100, 0), "Credits", font=fnt80bold, fill=fill)
        # KDA
        base_draw.text((x + 1500, 0), "K/D/A", font=fnt80bold, fill=fill)
        # Damage done
        base_draw.text((x + 1950, 0), "Damage", font=fnt80bold, fill=fill)
        # Damage taken
        base_draw.text((x + 2450, 0), "Taken", font=fnt80bold, fill=fill)
        # Objective time
        base_draw.text((x + 2900, 0), "Obj T.", font=fnt80bold, fill=fill)
        # base_draw.text((x + 2850, 60), "Time", font=fnt80, fill=fill)
        # Shielding
        base_draw.text((x + 3250, 0), "Shielding", font=fnt80bold, fill=fill)
        # Healing
        base_draw.text((x + 3750, 0), "Healing", font=fnt80bold, fill=fill)
        # Self Healing
        base_draw.text((x + 4220, 0), "Self Heal", font=fnt80bold, fill=fill)
        return key

    @classmethod
    # Creates a match image based on the two teams champions
    async def history_image(cls, team1, team2, t1_data, t2_data, r1, r2, match_data):
        shrink = 140
        image_size_y = 512 - shrink*2
        image_size_x = 512
        offset = 5
        history_image = Image.new(
            'RGBA', (image_size_x*10, image_size_y*12 + 264))
        # Adds the top key panel
        key = await helper.player_key_image(image_size_x, image_size_y)
        history_image.paste(key, (0, 0))
        # Creates middle panel
        mid_panel = await helper.middle_panel(match_data)
        history_image.paste(mid_panel, (0, 1392-40))
        # Adding in player data
        for i, (champ, champ2) in enumerate(zip(team1, team2)):
            if champ == "yagorath":
                champ_image = Image.open("home/ubuntu/icons/temp_card_art.png")
            else:
                sessions = aiohttp.ClientSession()
                url = await helper.get_champ_image(champ)
                async with sessions.get(url) as response:
                    resp = await response.read()
                    champ_image = Image.open(BytesIO(resp))
                sessions.close()
            border = (0, shrink, 0, shrink)  # left, up, right, bottom
            champ_image = ImageOps.crop(champ_image, border)
            rank_icon = Image.open(f"home/ubuntu/icons/ranks/{r1[i]}.png")
            # history_image.paste(champ_image, (0, image_size*i, image_size, image_size*(i+1)))
            player_panel = await helper.stats_image(champ_image, rank_icon, t1_data[i], i)
            history_image.paste(player_panel, (0, (image_size_y+10)*i+132))
            # Second team
            if champ == "yagorath":
                champ_image = Image.open("home/ubuntu/icons/temp_card_art.png")
            else:
                sessions = aiohttp.ClientSession()
                url = await helper.get_champ_image(champ)
                async with sessions.get(url) as response:
                    resp = await response.read()
                    champ_image = Image.open(BytesIO(resp))
                sessions.close()
            border = (0, shrink, 0, shrink)  # left, up, right, bottom
            champ_image = ImageOps.crop(champ_image, border)
            rank_icon = Image.open(f"home/ubuntu/icons/ranks/{r2[i]}.png")
            player_panel = await helper.stats_image(champ_image, rank_icon, t2_data[i], i+offset-1)
            history_image.paste(
                player_panel, (0, image_size_y * (i+offset) + 704))
        # Base speed is 10 - seconds
        history_image = history_image.resize(
            (4608//2, 3048//2), Image.ANTIALIAS)           # 5 seconds
        # history_image = history_image.resize((4608 // 4, 3048 // 4), Image.ANTIALIAS)     # 2.5 secs but bad looking
        # Creates a buffer to store the image in
        final_buffer = BytesIO()
        # Store the pillow image we just created into the buffer with the PNG format
        history_image.save(final_buffer, "PNG")
        # seek back to the start of the buffer stream
        final_buffer.seek(0)
        return final_buffer

    @classmethod
    async def middle_panel(cls, md):
        middle_panel = Image.new('RGBA', (512*10, 512), color=(14, 52, 60))
        # Adding in map to image
        map_name = map_file_name = (md[3].strip().replace("Ranked ", "").replace(" (TDM)", "").replace(" (Onslaught)", "")
                                    .replace(" (Siege)", "")).replace("Practice ", "")
        if "WIP" in map_name:
            map_file_name = "test_maps"
            map_name = map_name.replace("WIP ", "")
        # Needed to catch weird-unknown map modes
        try:
            match_map = Image.open("home/ubuntu/icons/maps/{}.png".format(
                map_file_name.lower().replace(" ", "_").replace("'", "")))
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
        fnt100bold = ImageFont.truetype("/home/ubuntu/arialbd.ttf", 100)
        draw_panel.text((512 * 2 + rs, 0 + ds),
                        str(f"Winning Team: {md[0]}"), font=fnt100, fill=(255, 255, 255))
        draw_panel.text((512 * 2 + rs, 100 + ds), (str(md[1]) + " minutes"), font=fnt100,
                        fill=(255, 255, 255))
        draw_panel.text((512 * 2 + rs, 200 + ds),
                        str(md[2]), font=fnt100, fill=(255, 255, 255))
        draw_panel.text((512 * 2 + rs, 300 + ds), str(map_name),
                        font=fnt100, fill=(255, 255, 255))
        # Right shift
        rs = 100
        # Team 1
        draw_panel.text((512 * 5 + rs, ds), "Team 1 Score: ",
                        font=fnt100, fill=(255, 255, 255))
        draw_panel.text((512 * 5 + rs * 8, ds),
                        str(md[4]), font=fnt100bold, fill=(255, 255, 255))
        center = (512/2 - 130/2)
        center2 = (512/2 - 80/2)
        # VS
        draw_panel.text((512 * 6-150, 200), "VS",
                        font=fnt100bold, fill=(227, 34, 34))
        # Team 2
        draw_panel.text((512 * 5 + rs, 348), "Team 2 Score: ",
                        font=fnt100, fill=(255, 255, 255))
        draw_panel.text((512 * 5 + rs * 8, 348),
                        str(md[5]), font=fnt100bold, fill=(255, 255, 255))
        #  add in banned champs if it's a ranked match
        try:
            if md[6]:
                # Ranked bans
                draw_panel.text((512 * 7 + rs * 7, center2),
                                "Bans:", font=fnt100, fill=(255, 255, 255))
                # Team 1 Bans
                if md[6].name == "yagorath":
                    champ_icon = Image.open(
                        "home/ubuntu/icons/temp_card_art.png")
                    champ_icon.resize((200, 200))
                    middle_panel.paste(champ_icon, (512 * 9, ds))
                else:
                    sessions = aiohttp.ClientSession()
                    champ_url = await helper.get_champ_image(md[6].name)
                    async with sessions.get(champ_url) as response:
                        resp = await response.read()
                        champ_icon = Image.open(BytesIO(resp))
                    sessions.close()
                    champ_icon = champ_icon.resize((200, 200))
                    middle_panel.paste(champ_icon, (512 * 9, ds))
                if md[7].name == "yagorath":
                    champ_icon = Image.open(
                        "home/ubuntu/icons/temp_card_art.png")
                    champ_icon = champ_icon.resize((200, 200))
                    middle_panel.paste(champ_icon, (512 * 9 + 240, ds))
                else:
                    champ_url = await helper.get_champ_image(md[7].name)
                    async with sessions.get(champ_url) as response:
                        resp = await response.read()
                        champ_icon = Image.open(BytesIO(resp))
                    sessions.close()
                    champ_icon = champ_icon.resize((200, 200))
                    middle_panel.paste(champ_icon, (512 * 9 + 240, ds))
                # Team 2 Bans
                if md[8].name == "yagorath":
                    champ_icon = Image.open(
                        "home/ubuntu/icons/temp_card_art.png")
                    champ_icon = champ_icon.resize((200, 200))
                    middle_panel.paste(champ_icon, (512 * 9, ds+232))
                else:
                    champ_url = await helper.get_champ_image(md[8].name)
                    async with sessions.get(champ_url) as response:
                        resp = await response.read()
                        champ_icon = Image.open(BytesIO(resp))
                    sessions.close()
                    champ_icon = champ_icon.resize((200, 200))
                    middle_panel.paste(champ_icon, (512 * 9, ds+232))
				if md[9].name == "yagorath":
                    champ_icon = Image.open(
                        "home/ubuntu/icons/temp_card_art.png")
                    champ_icon = champ_icon.resize((200, 200))
                    middle_panel.paste(champ_icon, (512 * 9 + 240, ds+232))
                else:
                    champ_url = await helper.get_champ_image(md[9].name)
                    async with sessions.get(champ_url) as response:
                        resp = await response.read()
                        champ_icon = Image.open(BytesIO(resp))
                    sessions.close()
                    champ_icon = champ_icon.resize((200, 200))
                    middle_panel.paste(champ_icon, (512 * 9 + 240, ds+232))
        except IndexError:
            pass
        return middle_panel
