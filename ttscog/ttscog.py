from redbot.core import commands, checks, Config
from .helper import helper
from .custom import FFmpegPCMAudio
from io import BytesIO
import discord
from gtts import gTTS


class TTSCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Config.get_conf(self, 828282859272, force_registration=True)
        default_guild = {
            "channel": "",
            "lang": "en",
            "tld": "com"
        }
        self.db.register_guild(**default_guild)
        self._locks = []

    @commands.command()
    async def connect(self, ctx, channel: discord.VoiceChannel=None):
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                await ctx.send('No voice channel to join. Please either specify a valid voice channel or join one.')
                return
        vc = ctx.voice_client
        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                await ctx.send(f'Moving to channel: <{channel}> timed out.')
                return
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                await ctx.send(f'Connecting to channel: <{channel}> timed out.')
                return
        await ctx.send(f'Connected to: **{channel}**', delete_after=20)
        
    @commands.command()
    @checks.is_owner()
    async def setttschan(self, ctx, channel: discord.TextChannel):
        await self.db.guild(ctx.guild).channel.set(channel.id)
        await ctx.send(f"TTS channel has been set to {channel.name}")
        
    @commands.command()
    @checks.is_owner()
    async def setttslang(self, ctx, lang):
        await self.db.guild(ctx.guild).lang.set(lang)
        await ctx.send(f"TTS language set to {lang}")
        
    @commands.command()
    @checks.is_owner()
    async def setttstld(self, ctx, tld):
        await self.db.guild(ctx.guild).tld.set(tld)
        await ctx.send(f"TTSTld language set to {tld}")
    
    #@commands.command()
    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        channel = await self.db.guild(msg.guild).channel()
        if msg.channel.id != channel:
            return
        if msg.author == self.bot.user:
            return
    
        if msg.author in self._locks:
            # their message being processed
            return
        try:
            self._locks.append(msg.author)
            await msg.channel.send(msg.content)
            vc = msg.guild.voice_client # We use it more then once, so make it an easy variable
            if not vc:
                # We are not currently in a voice channel
                #await msg.channel.send("I need to be in a voice channel to do this, please use the connect command.")
                return
            lang = await self.db.guild(msg.guild).lang()
            tld = await self.db.guild(msg.guild).tld()
            # Lets prepare our text, and then save the audio file
            fp = BytesIO()
            tts = gTTS(text=f"{msg.author.name} said {msg.content}", lang=lang, tld=tld)
            tts.write_to_fp(fp)
            fp.seek(0)
            try:
                # Lets play that mp3 file in the voice channel
                vc.play(FFmpegPCMAudio(fp.read(), pipe = True))
            
                # Lets set the volume to 1
                vc.source = discord.PCMVolumeTransformer(vc.source)
                vc.source.volume = 100
            except:
                await msg.channel.send("Please wait for me to finish speaking.")
            #except Exception:
                #await msg.channel.send(traceback.format_exc())
        finally:
            self._locks.remove(msg.author)
            
            
    @commands.command()
    async def disconnect(self, ctx):
        vc = ctx.guild.voice_client
        if not vc:
            await ctx.channel.send("I am not in a voice channel.")
            return
        await vc.disconnect()
        await ctx.send("No one is talking, so bye 👋")
        
