from __future__ import annotations

import re
import asyncio
import traceback
from io import BytesIO
from typing import NamedTuple

import discord
from gtts import gTTS
from redbot.core import commands, checks, Config

from .custom import FFmpegPCMAudio


class TTSItem(NamedTuple):
    sentence: str
    msg: discord.Message


class SFX(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Config.get_conf(self, 828282859272, force_registration=True)
        default_guild = {
            "channel": "",
            "lang": "en",
            "tld": "com",
            "with_nick": "on",
            "speed": 1
        }
        self.db.register_guild(**default_guild)
        self.vc_queue: asyncio.Queue[TTSItem] = asyncio.Queue()
        self.vc_task = asyncio.create_task(self.vc_speaker())
        self.vc_lock = asyncio.Lock()

    def cog_unload(self):
        self.vc_task.cancel()

    @commands.command()
    async def connect(self, ctx, channel: discord.VoiceChannel = None):
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                await ctx.send(
                    "No voice channel to join. "
                    "Please either specify a valid voice channel or join one."
                )
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
    @checks.admin()
    async def ttschannel(self, ctx, channel: discord.TextChannel):
        await self.db.guild(ctx.guild).channel.set(channel.id)
        await ctx.send(f"TTS channel has been set to {channel.name}")

    @commands.command()
    @checks.admin()
    async def ttslang(self, ctx, lang):
        await self.db.guild(ctx.guild).lang.set(lang)
        await ctx.send(f"TTS language set to {lang}")

    @commands.command()
    @checks.admin()
    async def ttstld(self, ctx, tld):
        await self.db.guild(ctx.guild).tld.set(tld)
        await ctx.send(f"TTS language tld set to {tld}")

    @commands.command()
    @checks.admin()
    async def ttsname(self, ctx, msg):
        if msg != "on" and msg != "off":
            await ctx.send("Please input a valid on or off sentence.")
            return
        await self.db.guild(ctx.guild).with_nick.set(msg)
        await ctx.send(f"TTS name calling is set to {msg}")

    @commands.command()
    @checks.admin()
    async def ttscleardb(self, ctx):
        await self.db.clear_all()
        await ctx.send("The db has been wiped.")

    @commands.command()
    @checks.admin()
    async def ttsspeed(self, ctx, speed: float):
        s = [speed]
        if len(s) > 2:
            await ctx.send("This command only supports a 2 number int or float.")
            return
        if speed < 0.5:
            await ctx.send("Speed bellow 0.5 not supported.")
            return
        if speed > 2.0:
            await ctx.send("Speed above 2.0 not supported.")
            return
        await self.db.guild(ctx.guild).speed.set(speed)
        await ctx.send(f"TTS speech speed has been set to {speed}")

    def vc_callback(self, error: Exception, channel: discord.TextChannel):
        self.vc_lock.release()
        if not isinstance(error, discord.ClientException):
            tb_msg = ''.join(traceback.format_exception(None, error, error.__traceback__))
            asyncio.create_task(channel.send(f"```\n{tb_msg}\n```"))

    async def vc_speaker(self):
        while True:
            try:
                item = await self.vc_queue.get()
                guild = item.msg.guild
                vc: discord.VoiceClient = guild.voice_client
                if not (vc and vc.is_connected()):
                    continue
                lang = await self.db.guild(guild).lang()
                tld = await self.db.guild(guild).tld()
                speed = await self.db.guild(guild).speed()
                fp = BytesIO()
                tts = gTTS(text=item.sentence, lang=lang, tld=tld, slow=False)
                tts.write_to_fp(fp)
                fp.seek(0)
                # Lets play that mp3 file in the voice channel
                await self.vc_lock.acquire()
                vc = guild.voice_client
                if not (vc and vc.is_connected()):
                    self.vc_lock.release()
                    continue
                vc.play(
                    FFmpegPCMAudio(
                        fp.read(), pipe=True, options=f'-filter:a "atempo={speed}" -t 00:00:20'
                    ),
                    after=lambda error: self.vc_callback(error, item.msg.channel),
                )
                # Lets set the volume to 1
                vc.source = discord.PCMVolumeTransformer(vc.source)
                vc.source.volume = 1
            except discord.ClientException:
                self.vc_lock.release()
            except Exception:
                self.vc_lock.release()
                await item.msg.channel.send(f"```\n{traceback.format_exc()}\n```")

    # @commands.command()
    @commands.Cog.listener()
    async def on_message_without_command(self, msg: discord.Message):
        channel = await self.db.guild(msg.guild).channel()
        if msg.channel.id != channel:
            return
        if msg.author.bot:
            return
        # await msg.channel.send(msg.content)
        vc: discord.VoiceClient = msg.guild.voice_client
        if not (vc and vc.is_connected()):
            # We are not currently in a voice channel
            # Silently exit
            # await msg.channel.send(
            #     "I need to be in a voice channel to do this, please use the connect command."
            # )
            return
        # Lets prepare our text, and then save the audio file
        with_nick = await self.db.guild(msg.guild).with_nick()
        text = re.sub(r'<a?:(\w+):\d+?>', r'\1', msg.clean_content)
        text = re.sub(r'https?://[\w-]+(.[\w-]+)+\S*', '', text)
        if with_nick == "on":
            sentence = f"{msg.author.name} says: {text}"
        elif with_nick == "off":
            sentence = f"{text}"
        await self.vc_queue.put(TTSItem(sentence, msg))
        
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        guilds = await self.conf.all_guilds()
        for guild in guilds:
            guild = self.bot.get_guild(guild)
            channel_id = await self.db.guild(guild).channel()
            channel = self.bot.get_channel(channel_id)
            if not member.id == self.bot.user.id:
                return
            elif before.channel is None:
                voice = after.channel.guild.voice_client
                time = 0
                while True:
                    await asyncio.sleep(1)
                    time = time + 1
                    if voice.is_playing() and not voice.is_paused():
                        time = 0
                    if time == 10: #600
                        await voice.disconnect()
                        await channel.send("No one talked for the past 10 min, so bye 👋: Auto-Disconnecting")
                    if not voice.is_connected():
                        break

    @commands.command()
    async def disconnect(self, ctx):
        vc = ctx.guild.voice_client
        if not vc:
            await ctx.channel.send("I am not in a voice channel.")
            return
        await vc.disconnect()
        await ctx.send("No one is talking, so bye 👋")
