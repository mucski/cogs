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
                await ctx.send('No channel to join. Please either specify a valid channel or join one.')
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
