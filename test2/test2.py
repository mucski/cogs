from redbot.core import commands
import random
from discord import File

from PIL import Image, ImageDraw, ImageFont
import io

class Test2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test2(self, ctx):
        text = "Hello I am a test text"
        image = ""
        
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
            match_map = Image.open("icons/maps/{}.png".format(map_file_name.lower().replace(" ", "_").replace("'", "")))
        except FileNotFoundError:
            match_map = Image.open("icons/maps/test_maps.png")
    
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
                champ_image = Image.open("icons/champ_icons/{}.png".format(await convert_champion_name(str(md[6]))))
                champ_image = champ_image.resize((200, 200))
                middle_panel.paste(champ_image, (512 * 7 + rs, ds))
            except FileNotFoundError:
                pass
    
            try:
                champ_image = Image.open("icons/champ_icons/{}.png".format(await convert_champion_name(str(md[7]))))
                champ_image = champ_image.resize((200, 200))
                middle_panel.paste(champ_image, (512 * 7 + rs + 240, ds))
            except FileNotFoundError:
                pass
    
            # Team 2 Bans
            try:
                champ_image = Image.open("icons/champ_icons/{}.png".format(await convert_champion_name(str(md[8]))))
                champ_image = champ_image.resize((200, 200))
                middle_panel.paste(champ_image, (512 * 7 + rs, ds+232))
            except FileNotFoundError:
                pass
    
            try:
                champ_image = Image.open("icons/champ_icons/{}.png".format(await convert_champion_name(str(md[9]))))
                champ_image = champ_image.resize((200, 200))
                middle_panel.paste(champ_image, (512 * 7 + rs + 240, ds+232))
            except FileNotFoundError:
                pass
    
        return middle_panel
        
    async def create_player_stats_image(champ_icon, champ_stats, index, party, color=False):
        shrink = 140
        offset = 10
        image_size_y = 512 - shrink * 2
        img_x = 512
        middle = image_size_y/2 - 50
        im_color = (175, 238, 238, 0) if index % 2 == 0 else (196, 242, 242, 0)
        # color = (175, 238, 238)   # light blue
        # color = (196, 242, 242)     # lighter blue
        champ_stats_image = Image.new('RGBA', (img_x*9, image_size_y+offset*2), color=im_color)
    
        champ_stats_image.paste(champ_icon, (offset, offset), (offset, offset))
    
        platform = champ_stats[10]
        if platform == "XboxLive":
            platform_logo = Image.open("icons/xbox_logo.png").resize((100, 100), Image.ANTIALIAS)
            platform_logo = platform_logo.convert("RGBA")
            champ_stats_image.paste(platform_logo, (img_x + 175, int(middle) + 60), platform_logo)
        elif platform == "Nintendo Switch":
            platform_logo = Image.open("icons/switch_logo.png")
            width, height = platform_logo.size
            scale = .15
            platform_logo = platform_logo.resize((int(width * scale), int(height * scale)), Image.ANTIALIAS)
            platform_logo = platform_logo.convert("RGBA")
            champ_stats_image.paste(platform_logo, (img_x + 135, int(middle) + 45), platform_logo)
        elif platform == "PSN":
            platform_logo = Image.open("icons/ps4_logo.png").resize((100, 100), Image.ANTIALIAS)
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
        base_draw.text((img_x + 20, middle-40), str(champ_stats[0]), font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 80), fill=(0, 0, 0))
        base_draw.text((img_x + 20, middle+60), str(champ_stats[1]), font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 80), fill=(0, 0, 0))
    
        # Parties
        fill = (128, 0, 128) if color else (0, 0, 0)
        base_draw.text((img_x + 750, middle), party[champ_stats[9]], font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 100), fill=fill)
    
        # Credits/Gold earned
        fill = (218, 165, 32) if color else (0, 0, 0)
        base_draw.text((img_x + 900, middle), str(champ_stats[2]), font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 100), fill=fill)
    
        # KDA
        fill = (101, 33, 67) if color else (0, 0, 0)
        base_draw.text((img_x + 1300, middle), str(champ_stats[3]), font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 100), fill=fill)
    
        # Damage done
        fill = (255, 0, 0) if color else (0, 0, 0)
        base_draw.text((img_x + 1830, middle), str(champ_stats[4]), font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 100), fill=fill)
    
        # Damage taken
        fill = (220, 20, 60) if color else (0, 0, 0)
        base_draw.text((img_x + 2350, middle), str(champ_stats[5]), font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 100), fill=fill)
    
        # Objective time
        fill = (159, 105, 52) if color else (0, 0, 0)
        base_draw.text((img_x + 2850, middle), str(champ_stats[6]), font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 100), fill=fill)
    
        # Shielding
        fill = (0, 51, 102) if color else (0, 0, 0)
        base_draw.text((img_x + 3150, middle), str(champ_stats[7]), font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 100), fill=fill)
    
        # Healing
        fill = (0, 128, 0) if color else (0, 0, 0)
        base_draw.text((img_x + 3600, middle), str(champ_stats[8]), font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 100), fill=fill)

        return champ_stats_image


    # Creates the text at the top of the image
    async def create_player_key_image(x, y, color=False):
        key = Image.new('RGB', (x * 9, y-100), color=(112, 225, 225))
        base_draw = ImageDraw.Draw(key)
        # ss = "Player Credits K/D/A  Damage  Taken  Objective Time  Shielding  Healing"
        base_draw.text((20, 0), "Champion", font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 80), fill=(0, 0, 0))
        base_draw.text((x + 20, 0), "Player", font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 80), fill=(0, 0, 0))
    
        # Parties
        fill = (128, 0, 128) if color else (0, 0, 0)
        base_draw.text((x + 750, 0), "P", font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 100), fill=fill)
    
        # Credits/Gold earned
        fill = (218, 165, 32) if color else (0, 0, 0)
        base_draw.text((x + 900, 0), "Credits", font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 80), fill=fill)
    
        # KDA
        fill = (101, 33, 67) if color else (0, 0, 0)
        base_draw.text((x + 1300, 0), "K/D/A", font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 80), fill=fill)
    
        # Damage done
        fill = (255, 0, 0) if color else (0, 0, 0)
        base_draw.text((x + 1830, 0), "Damage", font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 80), fill=fill)
    
        # Damage taken
        fill = (220, 20, 60) if color else (0, 0, 0)
        base_draw.text((x + 2350, 0), "Taken", font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 80), fill=fill)
    
        # Objective time
        fill = (159, 105, 52) if color else (0, 0, 0)
        base_draw.text((x + 2800, 0), "Objective", font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 60), fill=fill)
        base_draw.text((x + 2850, 60), "Time", font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 60), fill=fill)
    
        # Shielding
        fill = (0, 51, 102) if color else (0, 0, 0)
        base_draw.text((x + 3150, 0), "Shielding", font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 80), fill=fill)
    
        # Healing
        fill = (0, 128, 0) if color else (0, 0, 0)
        base_draw.text((x + 3600, 0), "Healing", font=ImageFont.truetype("/home/music166/mucski/arial.ttf", 80), fill=fill)

        return key
        
    @commands.command()
    async def canvas(self, ctx, text=None):
    
        IMAGE_WIDTH = 600
        IMAGE_HEIGHT = 400
    
        # create empty image 600x300 
        image = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT)) # RGB, RGBA (with alpha), L (grayscale), 1 (black & white)
    
        # or load existing image
        #image = Image.open('/home/furas/images/lenna.png')
    
        # create object for drawing
        draw = ImageDraw.Draw(image)
    
        # draw red rectangle with green outline from point (50,50) to point (550,250) #(600-50, 300-50)
        #draw.rectangle([50, 50, IMAGE_WIDTH-50, IMAGE_HEIGHT-50], fill=(255,0,0), outline=(0,0,0))
        draw.rectangle([0, 100, 600, 100], fill=(255,0,0))
    
        # draw text in center
        #text = f'Hello {ctx.author.name}'

        font = ImageFont.truetype('/home/music166/mucski/arial.ttf', 12)
    
        text_width, text_height = draw.textsize(text, font=font)
        x = (IMAGE_WIDTH - text_width)//2
        y = (IMAGE_HEIGHT - text_height)//2
    
        draw.text( (x, y), text, fill=(0,0,255), font=font)
    
        # create buffer
        buffer = io.BytesIO()
    
        # save PNG in buffer
        image.save(buffer, format='JPEG')    
    
        # move to beginning of buffer so `send()` it will read from beginning
        buffer.seek(0) 
    
        # send image
        await ctx.send(file=File(buffer, 'yourmom.jpg'))