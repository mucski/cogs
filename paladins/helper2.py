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
