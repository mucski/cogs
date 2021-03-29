from PIL import ImageOps, ImageDraw, Image, ImageFont
import aiohttp
from io import BytesIO




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
	    url = "https://raw.githubusercontent.com/EthanHicks1/PaladinsArtAssets/master/champ_icons/" \
	        + str(champ) + ".png"
	    return url


	@classmethod
	async def get_rank_image(cls, rank):
		pass


	@classmethod
	async def stats_image(cls, champ_icon, champ_stats, index, party):
	    shrink = 140
	    offset = 10
	    image_size_y = 512 - shrink * 2
	    img_x = 512
	    middle = image_size_y/2 - 50
	    im_color = (14, 34, 43) if index % 2 == 0 else (15, 40, 48)
	    img = Image.new("RGB", (img_x*10, image_size_y+offset*2), color=im_color)
	    img.paste(champ_icon, (offset, offset))
	    if champ_stats[12] == None:
	    	rank_icon == ""
	   	else:
	    	rank_icon = Image.open(f"home/ubuntu/icons/ranks/{champ_stats[12]}.png")
	    	rank_icon = rank_icon.resize(200, 200)
	    	img.paste(rank_icon, (offset, offset + 600))
	    draw = ImageDraw.Draw(img)
	    fnt80 = ImageFont.truetype("home/ubuntu/arial.ttf", 80)
	    fnt100 = ImageFont.truetype("home/ubuntu/arial.ttf", 100)
	    fnt80bold= ImageFont.truetype("home/ubuntu/arialbd.ttf", 80)
	    fill = (255, 255, 255)
	    if champ_stats[0] == "":
	        champ_stats[0] = "???????"
	    # Champion name, player name
	    draw.text((img_x+20, middle-40), str(champ_stats[0]), font=fnt80bold, fill=fill)
	    draw.text((img_x+20, middle+60), str(champ_stats[1]), font=fnt80, fill=fill)
	    # Rank
	    draw.text((img_x+750, middle), rank_icon, font=fnt100, fill=fill)
	    # Parties
	    draw.text((img_x+750, middle), str(champ_stats[9]), font=fnt100, fill=fill)
	    # Credits
	    draw.text((img_x+900, middle), str(champ_stats[2]), font=fnt100, fill=fill)
	    # KDA
	    draw.text((img_x+1300, middle), str(champ_stats[3]), font=fnt100, fill=fill)
	    # Damage Done
	    draw.text((img_x+1830, middle), str(champ_stats[4]), font=fnt100, fill=fill)
	    # Mitigated
	    draw.text((img_x+2350, middle), str(champ_stats[5]), font=fnt100, fill=fill)
	    # OBJ time
	    draw.text((img_x+2850, middle), str(champ_stats[6]), font=fnt100, fill=fill)
	    # Shielding
	    draw.text((img_x+3150, middle), str(champ_stats[7]), font=fnt100, fill=fill)
	    # Healing
	    draw.text((img_x+3600, middle), str(champ_stats[8]), font=fnt100, fill=fill)
	    # Self Healing
	    draw.text((img_x+4120, middle), str(champ_stats[11]), font=fnt100, fill=fill)
	    return img


	@classmethod
	async def player_key_image(cls, x, y):
	    key = Image.new("RGB", (x*10, y-100), color=(8, 21, 25))
	    base_draw = ImageDraw.Draw(key)
	    fill = (255, 255, 255)
	    fnt80bold= ImageFont.truetype("home/ubuntu/arialbd.ttf", 80)
	    # fnt100 = ImageFont.truetype("home/ubuntu/arial.ttf", 100)
	    # ss = "Player Credits K/D/A  Damage  Taken  Objective Time  Shielding  Healing"
	    base_draw.text((20, 0), "Champion", font=fnt80bold, fill=(255, 255, 255))
	    base_draw.text((x + 20, 0), "Player", font=fnt80bold, fill=(255, 255, 255))
	    # Ranks
	    base_draw.text((x + 750, 0), "R", font=fnt80bold, fill=fill)
	    # Parties
	    base_draw.text((x + 1000, 0), "P", font=fnt80bold, fill=fill)
	    # Credits/Gold earned
	    base_draw.text((x + 1250, 0), "Credits", font=fnt80bold, fill=fill)
	    # KDA
	    base_draw.text((x + 1700, 0), "K/D/A", font=fnt80bold, fill=fill)
	    # Damage done
	    base_draw.text((x + 1930, 0), "Damage", font=fnt80bold, fill=fill)
	    # Damage taken
	    base_draw.text((x + 2450, 0), "Taken", font=fnt80bold, fill=fill)
	    # Objective time
	    base_draw.text((x + 2900, 0), "Obj T.", font=fnt80bold, fill=fill)
	    # base_draw.text((x + 2850, 60), "Time", font=fnt80, fill=fill)
	    # Shielding
	    base_draw.text((x + 3250, 0), "Shielding", font=fnt80bold, fill=fill)
	    # Healing
	    base_draw.text((x + 3700, 0), "Healing", font=fnt80bold, fill=fill)
	    # Self Healing
	    base_draw.text((x + 4220, 0), "Self Healing", font=fnt80bold, fill=fill)
	    return key


	@classmethod
	# Creates a match image based on the two teams champions
	async def history_image(cls, team1, team2, t1_data, t2_data, p1, p2, match_data):
	    shrink = 140
	    image_size_y = 512 - shrink*2
	    image_size_x = 512
	    offset = 5
	    history_image = Image.new('RGB', (image_size_x*10, image_size_y*12 + 264))
	    # Adds the top key panel
	    key = await helper.player_key_image(image_size_x, image_size_y)
	    history_image.paste(key, (0, 0))
	    # Creates middle panel
	    mid_panel = await helper.middle_panel(match_data)
	    history_image.paste(mid_panel, (0, 1392-40))
	    # Adding in player data
	    for i, (champ, champ2) in enumerate(zip(team1, team2)):
	        try:
	            sessions = aiohttp.ClientSession()
	            url = await helper.get_champ_image(champ)
	            async with sessions.get(url) as response:
	                resp = await response.read()
	                champ_image = Image.open(BytesIO(resp))
	            sessions.close()
	        except FileNotFoundError:
	            champ_image = Image.open("icons/temp_card_art.png")
	        border = (0, shrink, 0, shrink)  # left, up, right, bottom
	        champ_image = ImageOps.crop(champ_image, border)
	        # history_image.paste(champ_image, (0, image_size*i, image_size, image_size*(i+1)))
	        player_panel = await helper.stats_image(champ_image, t1_data[i], i, p1)
	        history_image.paste(player_panel, (0, (image_size_y+10)*i+132))
	        # Second team
	        try:
	            sessions = aiohttp.ClientSession()
	            url = await helper.get_champ_image(champ2)
	            async with sessions.get(url) as response:
	                resp = await response.read()
	                champ_image = Image.open(BytesIO(resp))
	            sessions.close()
	        except FileNotFoundError:
	            champ_image = Image.open("icons/temp_card_art.png")
	        border = (0, shrink, 0, shrink)  # left, up, right, bottom
	        champ_image = ImageOps.crop(champ_image, border)

	        player_panel = await helper.stats_image(champ_image, t2_data[i], i+offset-1, p2)
	        history_image.paste(player_panel, (0, image_size_y * (i+offset) + 704))
	    # Base speed is 10 - seconds
	    history_image = history_image.resize((4608//2, 3048//2), Image.ANTIALIAS)           # 5 seconds
	    # history_image = history_image.resize((4608 // 4, 3048 // 4), Image.ANTIALIAS)     # 2.5 secs but bad looking
	    # Creates a buffer to store the image in
	    final_buffer = BytesIO()
	    # Store the pillow image we just created into the buffer with the PNG format
	    history_image.save(final_buffer, "JPEG")
	    # seek back to the start of the buffer stream
	    final_buffer.seek(0)
	    return final_buffer


	@classmethod
	async def middle_panel(cls, md):
	    middle_panel = Image.new('RGB', (512*10, 512), color=(14, 52, 60))
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
	    fnt100bold = ImageFont.truetype("/home/ubuntu/arialbd.ttf", 100)
	    draw_panel.text((512 * 2 + rs, 0 + ds), str(f"Winning Team: {md[0]}"), font=fnt100, fill=(255, 255, 255))
	    draw_panel.text((512 * 2 + rs, 100 + ds), (str(md[1]) + " minutes"), font=fnt100,
	                    fill=(255, 255, 255))
	    draw_panel.text((512 * 2 + rs, 200 + ds), str(md[2]), font=fnt100, fill=(255, 255, 255))
	    draw_panel.text((512 * 2 + rs, 300 + ds), str(map_name), font=fnt100, fill=(255, 255, 255))
	    # Right shift
	    rs = 100
	    # Team 1
	    draw_panel.text((512 * 5 + rs, ds), "Team 1 Score: ", font=fnt100, fill=(255, 255, 255))
	    draw_panel.text((512 * 5 + rs * 8, ds), str(md[4]), font=fnt100bold, fill=(255, 255, 255))
	    center = (512/2 - 130/2)
	    center2 = (512/2 - 80/2)
	    # VS
	    draw_panel.text((512 * 6-150, 200), "VS", font=fnt100bold, fill=(227, 34, 34))
	    # Team 2
	    draw_panel.text((512 * 5 + rs, 348), "Team 2 Score: ", font=fnt100, fill=(255, 255, 255))
	    draw_panel.text((512 * 5 + rs * 8, 348), str(md[5]), font=fnt100bold, fill=(255, 255, 255))
	    #  add in banned champs if it's a ranked match
	    try:
	        if md[6]:
	            # Ranked bans
	            draw_panel.text((512 * 7 + rs * 7, center2), "Bans:", font=fnt100, fill=(255, 255, 255))
	            # Team 1 Bans
	            try:
	                sessions = aiohttp.ClientSession()
	                champ_url = await helper.get_champ_image(md[6].name)
	                async with sessions.get(champ_url) as response:
	                    resp = await response.read()
	                    champ_icon = Image.open(BytesIO(resp))
	                sessions.close()
	                champ_icon = champ_icon.resize((200, 200))
	                middle_panel.paste(champ_icon, (512 * 9, ds))
	            except FileNotFoundError:
	                pass

	            try:
	                champ_url = await helper.get_champ_image(md[7].name)
	                async with sessions.get(champ_url) as response:
	                    resp = await response.read()
	                    champ_icon = Image.open(BytesIO(resp))
	                sessions.close()
	                champ_icon = champ_icon.resize((200, 200))
	                middle_panel.paste(champ_icon, (512 * 9 + 240, ds))
	            except FileNotFoundError:
	                pass
	            # Team 2 Bans
	            try:
	                champ_url = await helper.get_champ_image(md[8].name)
	                async with sessions.get(champ_url) as response:
	                    resp = await response.read()
	                    champ_icon = Image.open(BytesIO(resp))
	                sessions.close()
	                champ_icon = champ_icon.resize((200, 200))
	                middle_panel.paste(champ_icon, (512 * 9, ds+232))
	            except FileNotFoundError:
	                pass
	            try:
	                champ_url = await helper.get_champ_image(md[9].name)
	                async with sessions.get(champ_url) as response:
	                    resp = await response.read()
	                    champ_icon = Image.open(BytesIO(resp))
	                sessions.close()
	                champ_icon = champ_icon.resize((200, 200))
	                middle_panel.paste(champ_icon, (512 * 9 + 240, ds+232))
	            except FileNotFoundError:
	                pass
	    except IndexError:
	        pass
	    return middle_panel
