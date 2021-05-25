from redbot.core import commands, checks
from .helper import helper
from io import BytesIO
import discord

from gtts import gTTS


class TTSCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def connect(self, ctx, channel=None):
        await helper.connect(ctx, channel)
        
    @commands.command()
    async def disconnect(self, ctx):
        await helper.disconnect(ctx)
    
    @commands.command()
    async def repeat(self, ctx, text=None):
        """
        A command which saves `text` into a speech file with
        gtts and then plays it back in the current voice channel.
    
        Params:
         - text [Optional]
            This will be the text we speak in the voice channel
        """
        if not text:
            # We have nothing to speak
            await ctx.send(f"Hey {ctx.author.mention}, I need to know what to say please.")
            return
    
        vc = ctx.voice_client # We use it more then once, so make it an easy variable
        if not vc:
            # We are not currently in a voice channel
            await ctx.send("I need to be in a voice channel to do this, please use the connect command.")
            return
    
        # Lets prepare our text, and then save the audio file
        tts = gTTS(text=text, lang="en")
        fp = BytesIO()
        tts.write_to_fp(fp, format="mp3")
        fp.seek(0)
        # tts.save("text.mp3")
    
        try:
            # Lets play that mp3 file in the voice channel
            vc.play(discord.FFmpegPCMAudio(fp), after=lambda e: print(f"Finished playing: {e}"))
    
            # Lets set the volume to 1
            vc.source = discord.PCMVolumeTransformer(vc.source)
            vc.source.volume = 1
    
        # Handle the exceptions that can occur
        except ClientException as e:
            await ctx.send(f"A client exception occured:\n`{e}`")
        except TypeError as e:
            await ctx.send(f"TypeError exception:\n`{e}`")
        except OpusNotLoaded as e:
            await ctx.send(f"OpusNotLoaded exception:\n`{e}`")