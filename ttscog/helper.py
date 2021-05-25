import asyncio
import discord

class helper:

    @classmethod
    async def connect(cls, ctx, channel: discord.VoiceChannel=None):
        """
        Connect to a voice channel
        This command also handles moving the bot to different channels.
    
        Params:
        - channel: discord.VoiceChannel [Optional]
            The channel to connect to. If a channel is not specified, an attempt to join the voice channel you are in
            will be made.
        """
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
        
        
    @classmethod
    async def disconnect(cls, ctx):
        """
        Disconnect from a voice channel, if in one
        """
        vc = ctx.voice_client
    
        if not vc:
            await ctx.send("I am not in a voice channel.")
            return
    
        await vc.disconnect()
        await ctx.send("I have left the voice channel!")

    async def _latest_message_check(self, channel):
        async for message in self.bot.logs_from(channel, limit=self._latest_message_check_message_limit, reverse=True):
            delta = datetime.datetime.utcnow() - message.timestamp
            if delta.total_seconds() < self._latest_message_check_wait_limit and message.author.id != self.bot.user.id:
                if channel.id in self.paused_games:
                    self.paused_games.remove(channel.id)
                return True