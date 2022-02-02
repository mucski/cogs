from __future__ import annotations

import re
import asyncio
import traceback
from io import BytesIO
from typing import Optional, NamedTuple

import discord
from gtts import gTTS
from redbot.core.commands import Context
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
            "channel": 0,
            "lang": "en",
            "tld": "com",
            "with_nick": 1,
            "speed": 1
        }
        self.db.register_guild(**default_guild)
        self.vc_queue: asyncio.Queue[TTSItem] = asyncio.Queue()
        self.vc_task = asyncio.create_task(self.vc_speaker())
        self.vc_lock = asyncio.Lock()

    def cog_unload(self):
        self.vc_task.cancel()

    @commands.command()
    @commands.guild_only()
    async def connect(self, ctx: Context, channel: discord.VoiceChannel = None):
        if channel is None:
            voice_state: Optional[discord.VoiceState] = ctx.author.voice
            if voice_state is None:
                await ctx.send(
                    "No voice channel to join. "
                    "Please either specify a valid voice channel or join one."
                )
                return
            channel = voice_state.channel
        vc: Optional[discord.VoiceClient] = ctx.voice_client
        if vc is not None:
            # move to the channel
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                await ctx.send(f'Moving to channel: <{channel}> timed out.')
                return
        else:
            # join the channel
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                await ctx.send(f'Connecting to channel: <{channel}> timed out.')
                return
        await ctx.send(f'Connected to: **{channel}**', delete_after=20)

    @commands.command()
    @checks.admin()
    @commands.guild_only()
    async def ttschannel(self, ctx: Context, channel: discord.TextChannel):
        await self.db.guild(ctx.guild).channel.set(channel.id)
        await ctx.send(f"TTS channel has been set to {channel.name}")

    @commands.command()
    @checks.admin()
    @commands.guild_only()
    async def ttslang(self, ctx: Context, lang: str):
        await self.db.guild(ctx.guild).lang.set(lang)
        await ctx.send(f"TTS language set to {lang}")

    @commands.command()
    @checks.admin()
    @commands.guild_only()
    async def ttstld(self, ctx: Context, tld: str):
        await self.db.guild(ctx.guild).tld.set(tld)
        await ctx.send(f"TTS language tld set to {tld}")

    @commands.command()
    @checks.admin()
    @commands.guild_only()
    async def ttsname(self, ctx: Context, state: bool):
        await self.db.guild(ctx.guild).with_nick.set(state)
        await ctx.send(f"TTS name calling is set to {'ON' if state else 'OFF'}")

    @commands.command()
    @checks.admin()
    @commands.guild_only()
    async def ttscleardb(self, ctx: Context):
        await self.db.guild(ctx.guild).clear()
        await ctx.send("The db has been wiped.")

    @commands.command()
    @checks.admin()
    @commands.guild_only()
    async def ttsspeed(self, ctx: Context, speed: float):
        if speed > 2:
            await ctx.send("This command only supports a 2 number int or float.")
            return
        elif speed < 0.5:
            await ctx.send("Speed bellow 0.5 not supported.")
            return
        await self.db.guild(ctx.guild).speed.set(speed)
        await ctx.send(f"TTS speech speed has been set to {speed}")

    def vc_callback(self, error: Optional[Exception], channel: discord.TextChannel):
        if self.vc_lock.locked:
            self.vc_lock.release()
        if error is not None and not isinstance(error, discord.ClientException):
            tb_msg = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
            asyncio.create_task(channel.send(f"```\n{tb_msg}\n```"))

    async def vc_speaker(self):
        while True:
            try:
                item = await self.vc_queue.get()
                await self.vc_lock.acquire()
                guild: discord.Guild = item.msg.guild  # has to be there
                vc: Optional[discord.VoiceClient] = guild.voice_client
                if vc is None or not vc.is_connected():
                    continue
                lang = await self.db.guild(guild).lang()
                tld = await self.db.guild(guild).tld()
                speed = await self.db.guild(guild).speed()
                fp = BytesIO()
                tts = gTTS(text=item.sentence, lang=lang, tld=tld, slow=False)
                tts.write_to_fp(fp)
                fp.seek(0)
                # Lets play that mp3 file in the voice channel
                vc.play(
                    FFmpegPCMAudio(
                        fp.read(), pipe=True, options=f'-filter:a "atempo={speed}" -t 00:00:20'
                    ),
                    after=lambda error: self.vc_callback(error, item.msg.channel),
                )
                # Lets set the volume to 1
                vc.source = discord.PCMVolumeTransformer(vc.source)
                vc.source.volume = 1
            except Exception:
                await item.msg.channel.send(f"```\n{traceback.format_exc()}\n```")
            finally:
                if self.vc_lock.locked:
                    self.vc_lock.release()

    # @commands.command()
    @commands.Cog.listener()
    async def on_message_without_command(self, msg: discord.Message):
        if msg.author.bot:
            return
        guild: Optional[discord.Guild] = msg.guild
        if guild is None:
            # ignore messages in DMs
            return
        channel_id = await self.db.guild(guild).channel()
        if not channel_id:
            # channel isn't set
            return
        if msg.channel.id != channel_id:
            # message isn't in the set channel
            return
        # await msg.channel.send(msg.content)
        vc: Optional[discord.VoiceClient] = guild.voice_client
        if vc is None or not vc.is_connected():
            # We are not currently in a voice channel
            # Silently exit
            # await msg.channel.send(
            #     "I need to be in a voice channel to do this, please use the connect command."
            # )
            return
        # Lets prepare our text, and then save the audio file
        with_nick = await self.db.guild(guild).with_nick()
        text = re.sub(r'<a?:(\w+):\d+?>', r'\1', msg.clean_content)
        text = re.sub(r'https?://[\w-]+(.[\w-]+)+\S*', '', text)
        if with_nick:
            sentence = f"{msg.author.name} says: {text}"
        else:
            sentence = f"{text}"
        await self.vc_queue.put(TTSItem(sentence, msg))

    @commands.command()
    @commands.guild_only()
    async def disconnect(self, ctx: Context):
        vc: Optional[discord.VoiceClient] = ctx.guild.voice_client
        if vc is None:
            await ctx.channel.send("I am not in a voice channel.")
            return
        await vc.disconnect()
        await ctx.send("No one is talking, so bye 👋")
