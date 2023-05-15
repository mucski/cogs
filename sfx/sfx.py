from __future__ import annotations

import re
import asyncio
import traceback
from io import BytesIO
from typing import Optional, List, Dict, NamedTuple
import discord
from redbot.core.commands import Context
from redbot.core import commands, checks, Config, app_commands
from .custom import FFmpegPCMAudio

# Gevent patch before gTTS
try:
    import gevent
    gevent.monkey.patch_all()
except ModuleNotFoundError:
    pass
from gtts import gTTS

class TTSItem(NamedTuple):
    sentence: str
    msg: discord.Message


class SFX(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Config.get_conf(self, 828282859272, force_registration=True)
        default_guild = {
            "channels": [],
            "lang": "en",
            "tld": "com",
            "with_nick": 1,
            "speed": 1,
        }
        self.db.register_guild(**default_guild)
        self.vc_queue: asyncio.Queue[TTSItem] = asyncio.Queue()
        self.vc_task = asyncio.create_task(self.vc_speaker())
        self.vc_lock = asyncio.Lock()
        self.leave_tasks: Dict[int, asyncio.Task[None]] = {}

    def cog_unload(self):
        self.vc_task.cancel()

    @commands.hybrid_command()
    @commands.guild_only()
    async def connect(self, ctx: Context, channel: discord.VoiceChannel = None):
        """
        Connect to the specified voice channel, or the channel you're currently in.
        """
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
        await ctx.tick()

    @commands.hybrid_group()
    async def sfx(self, ctx):
        """Settings and other stuff related to Mucski's TTS cog"""
        pass

    @sfx.command()
    @commands.guild_only()
    async def disconnect(self, ctx: Context):
        """
        Disconnect from the current voice channel.
        """
        vc: Optional[discord.VoiceClient] = ctx.guild.voice_client
        if vc is None:
            await ctx.channel.send("I am not in a voice channel.")
            return
        await vc.disconnect()
        await ctx.tick()

    @sfx.command()
    @checks.admin()
    @commands.guild_only()
    async def addchan(self, ctx: Context, channel: discord.TextChannel):
        """
        Add a TTS channel to the list of tracked channels.
        """
        channels: List[int]
        async with self.db.guild(ctx.guild).channels() as channels:
            channels.append(channel.id)
        await ctx.send(f"{channel.name} has been added to tts channel list.")

    @sfx.command()
    @checks.admin()
    @commands.guild_only()
    async def dellchan(self, ctx: Context, channel: discord.TextChannel):
        """
        Remove a TTS channel from the list of tracked channels.
        """
        channels: List[int]
        async with self.db.guild(ctx.guild).channels() as channels:
            channels.remove(channel.id)
        await ctx.send(f"{channel.name} has been removed from tts channels.")

    @sfx.command()
    @checks.admin()
    @checks.mod()
    @commands.guild_only()
    async def lang(self, ctx: Context, lang: str):
        """
        Change the TTS language to the one specified.
        """
        await self.db.guild(ctx.guild).lang.set(lang)
        await ctx.send(f"TTS language set to {lang}")

    @sfx.command()
    @checks.admin()
    @checks.mod()
    @commands.guild_only()
    async def tld(self, ctx: Context, tld: str):
        """
        Change the TLD of the TTS language to the one specified.

        TLD stands for Top Level Domain, and can be changed to whichever way you'd normally
        access Google with. Default TLD is "com", thus pointing at "google.com". Changing it to
        "de" would point at "google.de", for example. This can be used to vary the speech accent.
        """
        await self.db.guild(ctx.guild).tld.set(tld)
        await ctx.send(f"TTS language tld set to {tld}")

    @sfx.command()
    @checks.admin()
    @checks.mod()
    @commands.guild_only()
    async def speak_name(self, ctx: Context, state: bool):
        """
        Set if you want TTS to include the speaker's name.
        """
        await self.db.guild(ctx.guild).with_nick.set(state)
        await ctx.send(f"TTS name calling is set to {'ON' if state else 'OFF'}")

    @sfx.command()
    @checks.admin()
    @commands.guild_only()
    async def cleardb(self, ctx: Context):
        """
        Clear all settings for the current guild.
        """
        await self.db.guild(ctx.guild).clear()
        await ctx.send("The db has been wiped.")

    @sfx.command()
    @checks.admin()
    @checks.mod()
    @commands.guild_only()
    @app_commands.choices(speed=[
         app_commands.Choice(name="0.5", value=0.5),
         app_commands.Choice(name="0.6", value=0.6),
         app_commands.Choice(name="0.7", value=0.7),
         app_commands.Choice(name="0.8", value=0.8),
         app_commands.Choice(name="0.9", value=0.9),
         app_commands.Choice(name="1.0", value=1.0),
         app_commands.Choice(name="1.1", value=1.1),
         app_commands.Choice(name="1.2", value=1.2),
         app_commands.Choice(name="1.3", value=1.3),
         app_commands.Choice(name="1.4", value=1.4),
         app_commands.Choice(name="1.5", value=1.5),
    ])
    async def speed(self, ctx: Context, speed: app_commands.Choice[float]=None):
        """
        Changes playback speed. Any speed between 0.5 and 2.0 is supported.
        """
        await self.db.guild(ctx.guild).speed.set(speed.value)
        await ctx.send(f"TTS speech speed has been set to {speed.value}", ephemeral=False)

    def vc_callback(self, error: Optional[Exception], channel: discord.TextChannel):
        if self.vc_lock.locked():
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
            except discord.ClientException:
                # raised when the bot is already playing some other audio, possibly from
                # another cog, which we cannot control - ignore this item
                pass
            except Exception:
                await item.msg.channel.send(f"```\n{traceback.format_exc()}\n```")
                if self.vc_lock.locked():
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
        channels = await self.db.guild(msg.guild).channels()
        if msg.channel.id not in channels:
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

    # async def leaver(self, guild: discord.Guild):
    #     await asyncio.sleep(900)  # 15 minutes
    #     vc: Optional[discord.VoiceClient] = guild.voice_client
    #     if vc is not None:
    #         await vc.disconnect()
    #     if guild.id in self.leave_tasks:
    #         del self.leave_tasks[guild.id]

    @commands.Cog.listener()
    async def on_voice_state_update(
        self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState
    ):
        # ignore events for ourselves
        if member.id == self.bot.user.id:
            return
        # narrow down the exact type of event we're looking for here
        vc: Optional[discord.VoiceClient] = member.guild.voice_client
        if vc is None or not vc.is_connected():
            # we're not connected to a channel in that guild
            return
        before_channel: Optional[discord.VoiceChannel] = before.channel
        after_channel: Optional[discord.VoiceChannel] = after.channel
        if (
            # before and after channels are None
            before_channel is None and after_channel is None
            or (
                # or both channels are set and they're the same channel
                before_channel is not None
                and after_channel is not None
                and before_channel.id == after_channel.id
            )
        ):
            return
        if before_channel is not None and before_channel.id == vc.channel.id:
            # disconnected from the channel we're in
            num_members = sum(1 for m in vc.channel.members if not m.bot)
            if num_members > 0:
                # there's at least one non-bot person connected to the channel we're in
                return
            else:
                if vc is not None:
                    await vc.disconnect()
                else:
                    pass
        # elif after_channel is not None and after_channel.id == vc.channel.id:
        #     # connected to the channel we're in
        #     guild_id = member.guild.id
        #     if guild_id in self.leave_tasks:
        #         self.leave_tasks[guild_id].cancel()
        #         del self.leave_tasks[guild_id]