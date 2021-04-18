from PIL import ImageOps, ImageDraw, Image, ImageFont
import aiohttp
from io import BytesIO
from redbot.core.utils.chat_formatting import humanize_number

class helper2:
    
    @classmethod
    async def testing(cls):
        return "Hello World"
        
    @classmethod
    async def get_champ_icon(cls, champ):
        champ = champ.lower()
        if "bomb" in champ:
            champ = "bomb-king"
        if "sha" in champ:
            champ = "sha-lin"
        if "mal" in champ:
            champ = "maldamba"
        url = f"https://webcdn.hirezstudios.com/paladins/champion-icons/{champ}.jpg"
        return url

    @classmethod
    async def player_key(cls, data):
        width = 300
        height = 400
        color = (8, 21, 25)
        img = Image.new("RGBA", (width, height), color=color)
        draw = ImageDraw.Draw(img)
        fnt = ImageFont.truetype("home/ubuntu/arialbd.ttf", 12)
        draw.text((20, 0), "Champion", font=fnt, fill=(255, 255, 255))
        return img
        
    @classmethod
    async def create_image(cls, team, matchdata, bans):
        offset = 25
        height = 1080
        width = 1920
        color = (14, 34, 43)
        img = Image.new('RGBA', (width, height), color=color)
        draw = ImageDraw.Draw(img)
        player_key = await helper2.player_key("data")
        i = 0
        offset2 = 0
        while i < 5:
            img.paste(player_key, (offset + offset2, offset))
            offset2 += 300 + offset
            i += 1
        
        # Final image product
        final_buffer = BytesIO()
        # Store the pillow image we just created into the buffer with the PNG format
        img.save(final_buffer, "PNG")
        # seek back to the start of the buffer stream
        final_buffer.seek(0)
        return final_buffer