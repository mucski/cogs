import arez
import discord
import asyncio
import humanize
import pkg_resources
import time
from datetime import datetime
from redbot.core import commands
from tabulate import tabulate
from redbot.core.utils.chat_formatting import pagify
from redbot.core.utils.chat_formatting import box
import discord
from PIL import Image, ImageFont, ImageDraw, ImageOps
# import requests
from io import BytesIO
from datetime import datetime, timedelta
from pytz import timezone
import json
import textwrap
import os
import re
from redbot.core.data_manager import bundled_data_path

class  Hirez(commands.Cog):
    """
    Returns stats for Paladins made by Evil Mojo Studios
    Every command is subject to change and in constant development.
    Version: 0.1.24

    Developed by Mucski
    """
    def __init__(self, bot):
        self.bot = bot
        self.f = open("/home/music166/mucski/key.txt", "r")
        self.auth = self.f.readline()
        self.devid = self.f.readline()
        self.api = arez.PaladinsAPI(dev_id = self.devid.strip(), auth_key = self.auth.strip())
       
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

    # Converts champion names so they can be used to fetch champion images in a url
    async def convert_champion_name(self, champ_name, special=False):
        champ_name = champ_name.lower()
        # These are the special cases that need to be checked
        if "bomb" in champ_name:
            return "bomb-king"
        if "mal" in champ_name:
            if special:
                return "mal'damba"
            else:
                return "maldamba"
        if "sha" in champ_name:
            return "sha-lin"
        # else return the name passed in since its already correct
        return champ_name


    # Gets a url to the image of champion's name passed in
    async def get_champ_image(self, champ_name):
        champ_name = await self.convert_champion_name(champ_name)
        url = "https://raw.githubusercontent.com/EthanHicks1/PaladinsAssistantBot/master/icons/champ_icons{}.png"\
            .format(champ_name)
        # request = requests.get(url)
        # if request.status_code == 404:
        #    url = "https://raw.githubusercontent.com/EthanHicks1/PaladinsAssistantBot/master/icons/unknown.png"
        return url


    # Creates an team image by using champion Icons
    async def create_team_image(self, champ_list, ranks):
        champion_images = []

        while len(champ_list) != 5:
            champ_list.append("?")

        for champ in champ_list:
            if champ != "?" and champ is not None:
                try:
                    champion_images.append(Image.open("/home/music166/mucski/icons/champ_icons/{}.png".format(await convert_champion_name(champ))))
                except FileNotFoundError:
                    image_size = 512
                    base = Image.new('RGB', (image_size, image_size), "black")
                    icon = Image.open("/home/music166/mucski/icons/unknown.png")
                    icon = icon.resize((512, 352), Image.ANTIALIAS)
                    base.paste(icon, (0, 80))
                    champion_images.append(base)
            else:
                image_size = 512
                base = Image.new('RGB', (image_size, image_size), "black")
                icon = Image.open("/home/music166/mucski/icons/unknown.png")
                icon = icon.resize((512, 352), Image.ANTIALIAS)
                base.paste(icon, (0, 160))

                # put text on image
                base_draw = ImageDraw.Draw(base)
                base_draw.text((140, 10), "Bot", font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 140))
                champion_images.append(base)

        # Original Image size # print(width, height)
        image_size = 512
        scale = 1.5
        # champion_images.append(img.resize((image_size, image_size)))

        team_image = Image.new('RGB', (image_size * len(champion_images), image_size))
        for i, champ in enumerate(champion_images):
            team_image.paste(champ, (image_size*i, 0, image_size*(i+1), image_size))

            # Only try to use ranked icons if its a ranked match
            if ranks:
                if i < len(ranks):  # make sure we don't go out of bounds
                    rank = Image.open("/home/music166/mucski/icons/ranks/" + ranks[i] + ".png")  # this works
                    width, height = rank.size
                    rank = rank.resize((int(width * scale), int(height * scale)))
                    team_image.paste(rank, (0 + (image_size * i), 0), rank)  # Upper Left

        # Testing
        # team_image.show()

        # Creates a buffer to store the image in
        final_buffer = BytesIO()

        # Store the pillow image we just created into the buffer with the PNG format
        team_image.save(final_buffer, "png")

        # seek back to the start of the buffer stream
        final_buffer.seek(0)

        return final_buffer


    # Creates a match image based on the two teams champions
    async def create_match_image(self, team1, team2, ranks1, ranks2):
        # start = time.time()
        buffer1 = await self.create_team_image(team1, ranks1)
        buffer2 = await self.create_team_image(team2, ranks2)
        middle = await self.draw_match_vs()
        # end = time.time()
        # print("run1", end - start)

        """ Not really faster....
        start2 = time.time()
        buffer1, buffer2, middle = await asyncio.gather(
            create_team_image(team1, ranks1),
            create_team_image(team2, ranks2),
            draw_match_vs()
        )
        end2 = time.time()
        print("run2", end2 - start2)
        """

        offset = 128

        image_size = 512
        match_image = Image.new('RGB', (image_size * len(team1), image_size*2 + offset))

        # box – The crop rectangle, as a (left, upper, right, lower)- tuple.

        # Row 1
        match_image.paste(Image.open(buffer1), (0, 0, (image_size*len(team1)), image_size))

        # Middle row
        match_image.paste(Image.open(middle), (0, image_size, (image_size * len(team1)), image_size+offset))

        # Row 2
        match_image.paste(Image.open(buffer2), (0, image_size + offset, (image_size*len(team1)), image_size*2 + offset))

        #                                                                                       Base speed is 10 - seconds
        # match_image = match_image.resize((int(1280), int(576)), Image.ANTIALIAS)              # 5 seconds
        match_image = match_image.resize((1280, 576))                                           # 5 seconds (looks good)
        # match_image = match_image.resize((int(2560/3), int(1152/3)), Image.ANTIALIAS)         # 2-3 seconds
        # match_image = match_image.resize((int(2560 / 4), int(1152 / 4)), Image.ANTIALIAS)     # 2-3 seconds
        # match_image.show()

        # Creates a buffer to store the image in
        final_buffer = BytesIO()

        # Store the pillow image we just created into the buffer with the PNG format
        match_image.save(final_buffer, "png")

        # seek back to the start of the buffer stream
        final_buffer.seek(0)

        return final_buffer


    # Draws a question in place of missing information for images
    async def draw_match_vs(self):
        base = Image.new('RGB', (2560, 128), "black")

        # put text on image
        base_draw = ImageDraw.Draw(base)
        base_draw.text((1248, 32), "VS", font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 64))

        # Creates a buffer to store the image in
        final_buffer = BytesIO()

        # Store the pillow image we just created into the buffer with the PNG format
        base.save(final_buffer, "png")

        # seek back to the start of the buffer stream
        final_buffer.seek(0)

        return final_buffer


    async def create_card_image(self, card_image, champ_info, json_data, lang):
        image_size_x = 256
        image_size_y = 196
        x_offset = 28
        y_offset = 48
        champ_card_name = champ_info[0]
        champ_card_level = champ_info[1]

        # Load in the Frame image from the web
        # response = requests.get("https://web2.hirez.com/paladins/cards/frame-{}.png".format(champ_card_level))
        # card_frame = Image.open(BytesIO(response.content))
        card_frame = Image.open("/home/music166/mucski/icons/card_frames/{}.png".format(champ_card_level))
        frame_x, frame_y = card_frame.size

        # Create the image without any text (just frame and card image)
        image_base = Image.new('RGBA', (frame_x, frame_y), (0, 0, 0, 0))

        # Resizing images that don't match the common image size
        check_x, check_y = card_image.size
        if check_x != image_size_x or check_y != image_size_y:
            card_image = card_image.resize((image_size_x, image_size_y), Image.ANTIALIAS)

        image_base.paste(card_image, (x_offset, y_offset, image_size_x + x_offset, image_size_y + y_offset))
        image_base.paste(card_frame, (0, 0), card_frame)

        # Add in the Card Number
        draw = ImageDraw.Draw(image_base)
        draw.text((30, frame_y-56), champ_card_level, font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 44))

        try:
            desc = json_data[lang][champ_card_name]["card_desc"]
            cool_down = json_data[lang][champ_card_name]["card_cd"]

            # todo --- find all the cards that don't have the word scale in them and see if they follow the same format
            # some cards don't have the word "scale" in them because cool-down scales.
            if "scale" not in desc:
                pass
            else:
                # Scale of the card
                scale = re.search('=(.+?)\|', desc)
                scale = float(scale.group(1)) * int(champ_card_level)
                # Text area of the card we are going to replace
                replacement = re.search('{(.*?)}', desc)

                # Replacing the scaling text with the correct number
                # desc = desc.replace('{'+str(replacement.group(1))+'}', str(float(scale.group(1)) * int(champ_card_level)))
                desc = desc.replace('{' + str(replacement.group(1)) + '}', str(round(scale, 1)))

                # Removes the extra text at the start in-between [****]
                desc = re.sub("[\[].*?[\]]", '', desc)
        except KeyError:
            desc = "Card information missing from bot data."
            cool_down = 0
        except AttributeError:
            desc = "Couldn't find card description for some reason. Please report this."
            cool_down = 0

        # Add card name
        draw = ImageDraw.Draw(image_base)
        font = ImageFont.truetype("/home/music166/mucski/arial.ttf", 21)
        text_x, text_y = draw.textsize(champ_card_name, font=font)
        draw.text(((frame_x-text_x)/2, (frame_y-text_y)/2+20), champ_card_name, font=font)

        # Add card text
        draw = ImageDraw.Draw(image_base)
        font = ImageFont.truetype("/home/music166/mucski/arial.ttf", 18)
        lines = textwrap.wrap(desc, width=26)
        padding = 40
        for line in lines:
            text_x, text_y = draw.textsize(line, font=font)
            draw.text(((frame_x-text_x)/2, (frame_y - text_y) / 2 + padding+20), line, font=font, fill=(64, 64, 64))
            padding += 25

        # Add in cool down if needed
        if cool_down != 0:
            # add in number
            draw = ImageDraw.Draw(image_base)
            draw.text((int(frame_x/2)+2, frame_y - 66), str(cool_down), font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 30),
                    fill=(64, 64, 64))

            cool_down_icon = Image.open("/home/music166/mucski/icons/cool_down_icon.png")
            image_base.paste(cool_down_icon, (int(frame_x/2)-20, frame_y - 60), mask=cool_down_icon)

        # Final image saving steps
        # Creates a buffer to store the image in
        final_buffer = BytesIO()

        # Store the pillow image we just created into the buffer with the PNG format
        image_base.save(final_buffer, "png")

        # seek back to the start of the buffer stream
        final_buffer.seek(0)

        return final_buffer


    # Creates a image desks
    async def create_deck_image(self, player_name, champ_name, deck, lang):
        card_image_x = 314
        card_image_y = 479

        # Main image
        color = (0, 0, 0, 0)
        deck_image = Image.new('RGBA', (1570, 800), color=color)

        champ_name = await self.convert_champion_name(champ_name)
        try:
            champ_background = Image.open("/home/music166/mucski/icons/champ_headers/{}.png".format(champ_name)).convert('RGBA')
        except FileNotFoundError:
            champ_background = Image.open("/home/music166/mucski/icons/maps/test_maps.png").convert('RGBA')
        champ_background = champ_background.resize((1570, 800), Image.ANTIALIAS)
        deck_image.paste(champ_background, (0, 0))

        # Loop to add all the cards in
        for i, card in enumerate(deck.cards):
            card_m = str(card).split("(")
            number = str(card_m[1]).split(")")[0]
            info = [card_m[0].strip(), number]

            # open data file
            if "mal" in champ_name.lower():
                champ_name = "mal-damba"

            # Opens the json data that relates to the specific champion
            try:
                file_name = "/home/music166/mucski/icons/champ_card_desc_lang/{}.json".format(champ_name)
                # file_name = "icons/champ_card_desc/{}.json".format(champ_name)    # Just English
                with open(file_name, encoding='utf-8') as json_f:
                    json_data = json.load(json_f)
            except (IndexError, json.decoder.JSONDecodeError, FileNotFoundError):
                json_data = {}

            # Opens the image of the card
            try:
                if 'mal' in champ_name:
                    champ_name = "Mal'Damba"
                try:
                    en_card_name = json_data[lang][card_m[0].strip()]["card_name_en"]
                    en_card_name = en_card_name.strip().lower().replace(" ", "-").replace("'", "")
                except KeyError:
                    en_card_name = "Not implemented yet."

                card_icon_image = Image.open("/home/music166/mucski/icons/champ_cards/{}/{}.png".format(champ_name, en_card_name))
            except FileNotFoundError:
                card_icon_image = Image.open("/home/music166/mucski/icons/temp_card_art.png")

            card_icon = await self.create_card_image(card_icon_image, info, json_data, lang=lang)

            card_icon = Image.open(card_icon)
            deck_image.paste(card_icon, (card_image_x * i, 800-card_image_y), card_icon)

        color = (255, 255, 255)

        if "mal" in champ_name:
            champ_name = "Mal'Damba"
        else:
            champ_name = champ_name.upper()

        # Adding in other text on image
        draw = ImageDraw.Draw(deck_image)
        draw.text((0, 0), str(player_name), color, font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 64))
        draw.text((0, 64), str(champ_name), color, font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 64))
        draw.text((0, 128), str(deck.deckName), color, font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 64))

        # Creates a buffer to store the image in
        final_buffer = BytesIO()

        # Store the pillow image we just created into the buffer with the PNG format
        deck_image.save(final_buffer, "png")

        # seek back to the start of the buffer stream
        final_buffer.seek(0)

        return final_buffer


    # Creates a match image based on the two teams champions
    async def create_history_image(self, team1, team2, t1_data, t2_data, p1, p2, match_data, colored):
        shrink = 140
        image_size_y = 512 - shrink*2
        image_size_x = 512
        offset = 5
        history_image = Image.new('RGB', (image_size_x*9, image_size_y*12 + 264))

        # Adds the top key panel
        key = await self.create_player_key_image(image_size_x, image_size_y, colored)
        history_image.paste(key, (0, 0))

        # Creates middle panel
        mid_panel = await self.create_middle_info_panel(match_data)
        history_image.paste(mid_panel, (0, 1392-40))

        # Adding in player data
        for i, (champ, champ2) in enumerate(zip(team1, team2)):
            try:
                champ_image = Image.open("/home/music166/mucski/icons/champ_icons/{}.png".format(await self.convert_champion_name(champ)))
            except FileNotFoundError:
                champ_image = Image.open("/home/music166/mucski/icons/temp_card_art.png")
            border = (0, shrink, 0, shrink)  # left, up, right, bottom
            champ_image = ImageOps.crop(champ_image, border)
            # history_image.paste(champ_image, (0, image_size*i, image_size, image_size*(i+1)))
            player_panel = await self.create_player_stats_image(champ_image, t1_data[i], i, p1, colored)
            history_image.paste(player_panel, (0, (image_size_y+10)*i+132))

            # Second team
            try:
                champ_image = Image.open("/home/music166/mucski/icons/champ_icons/{}.png".format(await self.convert_champion_name(champ2)))
            except FileNotFoundError:
                champ_image = Image.open("/home/music166/mucski/icons/temp_card_art.png")
            border = (0, shrink, 0, shrink)  # left, up, right, bottom
            champ_image = ImageOps.crop(champ_image, border)

            player_panel = await self.create_player_stats_image(champ_image, t2_data[i], i+offset-1, p2, colored)
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


    async def create_middle_info_panel(self, md):  # update this section
        middle_panel = Image.new('RGB', (512*9, 512), color=(217, 247, 247))

        # Adding in map to image
        map_name = map_file_name = (md[3].strip().replace("Ranked ", "").replace(" (TDM)", "").replace(" (Onslaught)", "")
                                    .replace(" (Siege)", "")).replace("Practice ", "")
        if "WIP" in map_name:
            map_file_name = "test_maps"
            map_name = map_name.replace("WIP ", "")

        # Needed to catch weird-unknown map modes
        try:
            match_map = Image.open("/home/music166/mucski/icons/maps/{}.png".format(map_file_name.lower().replace(" ", "_").replace("'", "")))
        except FileNotFoundError:
            match_map = Image.open("/home/music166/mucski/icons/maps/test_maps.png")

        match_map = match_map.resize((512*2, 512), Image.ANTIALIAS)
        middle_panel.paste(match_map, (0, 0))

        # Preparing the panel to draw on
        draw_panel = ImageDraw.Draw(middle_panel)

        # Add in match information
        ds = 50  # Down Shift
        rs = 20  # Right Shift
        draw_panel.text((512 * 2 + rs, 0 + ds), str(md[0]), font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 100), fill=(0, 0, 0))
        draw_panel.text((512 * 2 + rs, 100 + ds), (str(md[1]) + " minutes"), font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 100),
                        fill=(0, 0, 0))
        draw_panel.text((512 * 2 + rs, 200 + ds), str(md[2]), font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 100), fill=(0, 0, 0))
        draw_panel.text((512 * 2 + rs, 300 + ds), str(map_name), font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 100), fill=(0, 0, 0))

        # Right shift
        rs = 100
        # Team 1
        draw_panel.text((512 * 4 + rs, ds), "Team 1 Score: ", font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 100), fill=(0, 0, 0))
        draw_panel.text((512 * 4 + rs * 8, ds), str(md[4]), font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 100), fill=(0, 0, 0))

        center = (512/2 - 130/2)
        center2 = (512/2 - 80/2)
        # VS
        draw_panel.text((512 * 5-150, center), "VS", font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 130), fill=(0, 0, 0))

        # Team 2
        draw_panel.text((512 * 4 + rs, 372), "Team 2 Score: ", font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 100), fill=(0, 0, 0))
        draw_panel.text((512 * 4 + rs * 8, 372), str(md[5]), font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 100), fill=(0, 0, 0))

        #  add in banned champs if it's a ranked match
        if md[6] is not None:
            # Ranked bans
            draw_panel.text((512 * 5 + rs * 8, center2), "Bans:", font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 80), fill=(0, 0, 0))

            # Team 1 Bans
            try:
                champ_image = Image.open("/home/music166/mucski/icons/champ_icons/{}.png".format(await self.convert_champion_name(str(md[6]))))
                champ_image = champ_image.resize((200, 200))
                middle_panel.paste(champ_image, (512 * 7 + rs, ds))
            except FileNotFoundError:
                pass

            try:
                champ_image = Image.open("/home/music166/mucski/icons/champ_icons/{}.png".format(await self.convert_champion_name(str(md[7]))))
                champ_image = champ_image.resize((200, 200))
                middle_panel.paste(champ_image, (512 * 7 + rs + 240, ds))
            except FileNotFoundError:
                pass

            # Team 2 Bans
            try:
                champ_image = Image.open("/home/music166/mucski/icons/champ_icons/{}.png".format(await self.convert_champion_name(str(md[8]))))
                champ_image = champ_image.resize((200, 200))
                middle_panel.paste(champ_image, (512 * 7 + rs, ds+232))
            except FileNotFoundError:
                pass

            try:
                champ_image = Image.open("/home/music166/mucski/icons/champ_icons/{}.png".format(await self.convert_champion_name(str(md[9]))))
                champ_image = champ_image.resize((200, 200))
                middle_panel.paste(champ_image, (512 * 7 + rs + 240, ds+232))
            except FileNotFoundError:
                pass

        return middle_panel


    async def create_player_stats_image(self, champ_icon, champ_stats, index, party, color=False):
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

        #platform = champ_stats[10]
        #if platform == "XboxLive":
        #    platform_logo = Image.open("/home/music166/mucski/icons/xbox_logo.png").resize((100, 100), Image.ANTIALIAS)
        #    platform_logo = platform_logo.convert("RGBA")
        #    champ_stats_image.paste(platform_logo, (img_x + 175, int(middle) + 60), platform_logo)
        #elif platform == "Nintendo Switch":
        #    platform_logo = Image.open("/home/music166/mucski/icons/switch_logo.png")
        #    width, height = platform_logo.size
        #    scale = .15
        #    platform_logo = platform_logo.resize((int(width * scale), int(height * scale)), Image.ANTIALIAS)
        #    platform_logo = platform_logo.convert("RGBA")
        #    champ_stats_image.paste(platform_logo, (img_x + 135, int(middle) + 45), platform_logo)
        #elif platform == "PSN":
        #    platform_logo = Image.open("/home/music166/mucski/icons/ps4_logo.png").resize((100, 100), Image.ANTIALIAS)
        #    platform_logo = platform_logo.convert("RGBA")
        #    champ_stats_image.paste(platform_logo, (img_x + 175, int(middle) + 60), platform_logo)
        # For future if I want to add a PC icon
        # else:
        #    print("PC")

        # if platform_logo:
        #    platform_logo = platform_logo.convert("RGBA")
        #    champ_stats_image.paste(platform_logo, (img_x + 175, int(middle)+60), platform_logo)
        #    # champ_stats_image.show()

        base_draw = ImageDraw.Draw(champ_stats_image)
        
        path = bundled_data_path(self)

        # Private account or unknown
        #if str(champ_stats[0]) == "":
            #champ_stats[0] = "*****"

        # Player name and champion name
        base_draw.text((img_x + 20, middle-40), str(champ_stats[0]), font=ImageFont.truetype(f"{path}/arial.ttf", 80), fill=(0, 0, 0))
        base_draw.text((img_x + 20, middle+60), str(champ_stats[1]), font=ImageFont.truetype(f"{path}/arial.ttf", 80), fill=(0, 0, 0))

        # Parties
        #fill = (128, 0, 128) if color else (0, 0, 0)
        #base_draw.text((img_x + 750, middle), "1", font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 100), fill=fill)

        # Credits/Gold earned
        #fill = (218, 165, 32) if color else (0, 0, 0)

        # KDA
        #fill = (101, 33, 67) if color else (0, 0, 0)
        #base_draw.text((img_x + 1300, middle), "23/4/24", font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 100), fill=fill)

        # Damage done
        #fill = (255, 0, 0) if color else (0, 0, 0)
        #base_draw.text((img_x + 1830, middle), "80000", font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 100), fill=fill)

        # Damage taken
        #fill = (220, 20, 60) if color else (0, 0, 0)
        #base_draw.text((img_x + 2350, middle), "0", font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 100), fill=fill)

        # Objective time
        #fill = (159, 105, 52) if color else (0, 0, 0)
        #base_draw.text((img_x + 2850, middle), "20", font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 100), fill=fill)

        # Shielding
        #fill = (0, 51, 102) if color else (0, 0, 0)
        #base_draw.text((img_x + 3150, middle), "0", font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 100), fill=fill)

        # Healing
        #fill = (0, 128, 0) if color else (0, 0, 0)
        #base_draw.text((img_x + 3600, middle), "20000", font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 100), fill=fill)

        return champ_stats_image


    # Creates the text at the top of the image
    async def create_player_key_image(self, x, y, color=False):
        key = Image.new('RGB', (x * 9, y-100), color=(112, 225, 225))
        base_draw = ImageDraw.Draw(key)
        fnt = ImageFont.truetype(f"{bundled_data_path(self)}/arial.ttf", 80)
        # ss = "Player Credits K/D/A  Damage  Taken  Objective Time  Shielding  Healing"
        base_draw.text((20, 0), "Champion", font=fnt, fill=(0, 0, 0))
        base_draw.text((x + 20, 0), "Player", font=fnt, fill=(0, 0, 0))

        # Parties
        fill = (128, 0, 128) if color else (0, 0, 0)
        base_draw.text((x + 750, 0), "P", font=fnt, fill=fill)

        # Credits/Gold earned
        fill = (218, 165, 32) if color else (0, 0, 0)
        base_draw.text((x + 900, 0), "Credits", font=fnt, fill=fill)

        # KDA
        fill = (101, 33, 67) if color else (0, 0, 0)
        base_draw.text((x + 1300, 0), "K/D/A", font=fnt, fill=fill)

        # Damage done
        fill = (255, 0, 0) if color else (0, 0, 0)
        base_draw.text((x + 1830, 0), "Damage", font=fnt, fill=fill)

        # Damage taken
        fill = (220, 20, 60) if color else (0, 0, 0)
        base_draw.text((x + 2350, 0), "Taken", font=fnt, fill=fill)

        # Objective time
        fill = (159, 105, 52) if color else (0, 0, 0)
        base_draw.text((x + 2800, 0), "Obj Time", font=fnt, fill=fill)
        # base_draw.text((x + 2850, 60), "Time", font=fnt, fill=fill)

        # Shielding
        fill = (0, 51, 102) if color else (0, 0, 0)
        base_draw.text((x + 3150, 0), "Shielding", font=fnt, fill=fill)

        # Healing
        fill = (0, 128, 0) if color else (0, 0, 0)
        base_draw.text((x + 3600, 0), "Healing", font=fnt, fill=fill)

        return key


    @commands.command()
    async def hitest(self, ctx):
        await ctx.send("Your mom")

    @commands.command()
    async def stats(self, ctx, player, platform = "pc"):
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
    async def matchimage(self, ctx, player, platform="pc"):
        platform = arez.Platform(platform)
        if platform is None:
            await ctx.send("Wrong platform")
            return
        if player.isdecimal():
            player = await self.api.get_player(player)
        else:
            player_obj = await self.api.search_players(player, platform)
            player = await player_obj[0]
        history = await player.get_match_history()
        last = history[0]
        match = await self.api.get_match(last.id, expand_players=True)
        match_info = [match.score, match.duration, match.region, match.map_name, match.score[0], match.score[1]]
        team1data = []
        team2data = []
        team1champs = []
        team2champs = []
        team1parties = []
        team2parties = []
        temp = match.bans
        # handles if they provide the color option and no match id
        try:
            match_id = int(match.id)
        except BaseException:
            colored = match.id
            match_id = -1
            
        new_party_id = 0
        for match_player in match.players:
            if match_player.team_number != 1:
                continue
            team1data.append([match_player.player.name, match_player.account_level, match_player.credits, match_player.kda_text,
                             match_player.damage_done, match_player.damage_taken, match_player.objective_time, match_player.damage_mitigated, 
                             match_player.healing_done, match_player.party_number, match_player.player.platform])
            team1champs.append(match_player.champion.name)
            team1parties.append(match_player.party_number)
        for match_player in match.players:
            if match_player.team_number != 2:
                continue
            team2data.append([match_player.player.name, match_player.account_level, match_player.credits, match_player.kda_text,
                             match_player.damage_done, match_player.damage_taken, match_player.objective_time, match_player.damage_mitigated, 
                             match_player.healing_done, match_player.party_number, match_player.player.platform])
            team2champs.append(match_player.champion.name)
            team2parties.append(match_player.party_number)
        color = False
        buffer = await self.create_history_image(team1champs, team2champs, team1data, team2data, team1parties, team2parties, (match_info + temp), color)
        file = discord.File(filename="Yourmom.png", fp=buffer)
        await ctx.send(file=file)
        
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