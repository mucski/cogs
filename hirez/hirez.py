import arez
import discord
import asyncio
import humanize
import pkg_resources
from datetime import datetime
from redbot.core import commands
from tabulate import tabulate
from redbot.core.utils.chat_formatting import pagify
from redbot.core.utils.chat_formatting import box
import time


class Hirez(commands.Cog):
    """
    Returns stats for Paladins made by Evil Mojo Studios
    
    Every command is subject to change and in constant development.
    """
    def __init__(self, bot):
        self.bot = bot
        self.f = open("/home/music166/mucski/key.txt", "r")
        self.auth = self.f.readline()
        self.devid = self.f.readline()
        self.api = arez.PaladinsAPI(dev_id = self.devid.strip(), auth_key = self.auth.strip())
       
    def cog_unload(self):
        asyncio.create_task(self.api.close())
        self.f.close()

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            exc = error.original
            if isinstance(exc, arez.Unavailable):
                await ctx.send("Hi-Rez API currently shat itself. Offline or unavailable.")
                return
            elif isinstance(exc, arez.Private):
                await ctx.send("The requested users profile is set to private.")
                return
            elif isinstance(exc, arez.NotFound):
                await ctx.send("Player was not found.")
                return
            elif isinstance(exc, IndexError):
                await ctx.send("Player did not play for over a month, therefore nothing to display.")
                return
            # elif isinstance(exc, ...):
            #     await ctx.send(...)
            #     return
        await ctx.bot.on_command_error(ctx, error, unhandled_by_cog=True)
        
    @commands.command()
    async def keytest(self, ctx):
        await ctx.send(f"{self.devid.strip()} - {self.auth.strip()}")

    @commands.command()
    async def stats(self, ctx, player, platform = "pc"):
        """Player stats, title, avatar and more"""
        platform = arez.Platform(platform)
        if platform is None:
            await ctx.send("Wrong platform buster!")
            return
        if player.isdecimal():
            player = await self.api.get_player(player)  
        else:
            player_obj = await self.api.search_players(player, platform)
            player = await player_obj[0]
        desc = (
            "**__Player Stats__**\n"
            f```"Account level: {player.level}\n"
            f"Playtime: {int(player.playtime.total_hours())} hours\n"
            f"Region: {player.region}\n"
            f"Champions Owned: {player.champion_count}\n"
            f"Achievements Unlocked: {player.total_achievements}\n```"
            "\n\n"
            "**__Casual Stats__**\n"
            f"Win Rate: {player.casual.wins} / {player.casual.losses} ({player.casual.winrate_text})\n"
            f"Deserted: {player.casual.leaves}\n"
            "\n\n"
            f"**__Ranked Stats Season {player.ranked_best.season}__**\n"
            f"Win Rate: {player.ranked_best.wins} / {player.ranked_best.losses} ({player.ranked_best.winrate_text})\n"
            f"Deserted: {player.ranked_best.leaves}\n"
            f"Ranked Type: {player.ranked_best.type}\n"
            f"Current Rank: {player.ranked_best.rank} ({player.ranked_best.points} TP)\n"
        )
        embed = discord.Embed(color=await self.bot.get_embed_color(ctx), title=f"Player ID: `{player.id}` Title: _{player.title}_")
        embed.description=desc
        embed.set_author(name=f"{player.name}({player.platform})")
        embed.set_thumbnail(url=player.avatar_url)
        #embed.add_field(name="Account level", value=player.level)
        #embed.add_field(name="Playtime", value=f"{int(player.playtime.total_hours())} hours")
        #embed.add_field(name="Region", value=player.region)
        #embed.add_field(name="Casual Winrate", value=f"{player.casual.wins} / {player.casual.losses} ({player.casual.winrate_text})")
        #embed.add_field(name="Ranked Winrate", value=f"{player.ranked_best.wins} / {player.ranked_best.losses} ({player.ranked_best.winrate_text})")
        #embed.add_field(name="Ranked type", value=player.ranked_best.type)
        #embed.add_field(name="Current rank", value=eye)
        embed.set_footer(text=f"Account created: {humanize.naturaltime(datetime.utcnow() - player.created_at)}, last seen: {humanize.naturaltime(datetime.utcnow() - player.last_login)}")
        await ctx.send(embed=embed)

    @commands.command()
    async def match(self, ctx, player, platform="pc"):
        """A match played by a player"""
        platform = arez.Platform(platform)
        if platform is None:
            await ctx.send("Wrong platform buster!")
            return
        if player.isdecimal():
            player = await self.api.get_player(player)
        else:
            player_obj = await self.api.search_players(player, platform)
            player = await player_obj[0]
        history = await player.get_match_history()
        last = history[0]
        match = await self.api.get_match(last.id)
        #Build embed
        e = discord.Embed(color=await self.bot.get_embed_color(ctx), title=f"Detailed match for {player.name}({player.platform})")
        e.add_field(name="Player ID / Player Level", value=f"``{player.id}`` / {player.level}")
        if last.champion is not None:
            e.set_thumbnail(url=last.champion.icon_url)
        else:
            e.set_thumbnail(url=ctx.author.avatar_url)
        e.add_field(name="Match", value=f"``{match.id}`` - {match.queue} - {match.map_name}")
        e.add_field(name="Duration / Region", value=f"{match.duration} / { match.region}")
        e.add_field(name="Score / Winning Team", value=f"{match.score} / ``Team {match.winning_team}``")
        e.add_field(name="Replay Available", value=f"{match.replay_available}")
        if match.bans:
            e.add_field(name="Banned champions:", value='\n'.join(ch.name for ch in match.bans), inline=False)
        else:
            pass
        e.add_field(name="Team 1\nPlayer Name / ID / KDA / Damage / Healing or Shielding", value='\n'.join(map(str, match.team1)).replace(f"{player.name}", f"``{player.name}``"), inline="False")
        e.add_field(name="Team 2\nPlayer Name / ID / KDA / Damage / Healing or Shielding", value='\n'.join(map(str, match.team2)).replace(f"{player.name}", f"``{player.name}``"), inline="False")
        e.set_footer(text=f"Played: {humanize.naturaltime(datetime.utcnow() - match.timestamp)}")
        #await ctx.send(embed=e)
        sex = await match.expand_players(match)
        await ctx.send(sex)

    @commands.command()
    async def current(self, ctx, player, platform="pc"):
        """A match played by a player"""
        platform = arez.Platform(platform)
        if platform is None:
            await ctx.send("Wrong platform buster!")
            return
        if player.isdecimal():
            player = await self.api.get_player(player)  
        else:
            player_obj = await self.api.search_players(player, platform)
            player = await player_obj[0]
        status = await player.get_status()
        match =  await status.get_live_match()
        if match is None:
            await ctx.send("Player not in a match")
            return
        #Build embed
        e = discord.Embed(color=await self.bot.get_embed_color(ctx), title=f"Current match for {player.name} - _{player.title}_")
        e.set_thumbnail(url=player.avatar_url)
        e.add_field(name="Match", value=f"``{match.id}`` - {match.queue} - {match.map_name} - { match.region}")
        #e.add_field(name="Blah", value=match.team1.player)
        e.add_field(name="Team 1\nPlayer Name / ID / KDA / Damage / Healing or Shielding", value='\n'.join(map(str, match.team1)).replace(f"{player.name}", f"``{player.name}``"), inline="False")
        e.add_field(name="Team 2\nPlayer Name / ID / KDA / Damage / Healing or Shielding", value='\n'.join(map(str, match.team2)).replace(f"{player.name}", f"``{player.name}``"), inline="False")
        await ctx.send(embed=e)        
        
    @commands.command()
    async def history(self, ctx, player, platform = "pc"):
        """Player history"""
        platform = arez.Platform(platform)
        if platform is None:
            await ctx.send("Wrong platform buster!")
            return
        if player.isdecimal():
            player = await self.api.get_player(player)
        else:
            player_obj = await self.api.search_players(player, platform)
            player = await player_obj[0]
        history = await player.get_match_history()
        matches = []
        for match in history: #[:30]
            matchlist = []
            if match.winner == True:
                matchlist.append("+ WON")
                matchlist.append(match)
            else:
                matchlist.append("- LOST")
                matchlist.append(match)
            matches.append(matchlist)
        
        table = tabulate(matches, headers=["# W/L", "QUEUE/CHAMPION/SCORE"])
        lenght = "\n".join(table)
        if len(lenght) < 2000:
            await ctx.send(box(table, lang='diff'))
        else:
            for page in pagify(table):
                await ctx.send(box(page, lang='diff'))
    
    @commands.command()
    async def status(self, ctx):
        #status = arez.ServerStatus(statuses)
        status2 = self.api.get_server_status
        await ctx.send(status2)
    
    @commands.command()
    async def last(self, ctx, player, platform = "pc"):
        start_time = time.time()
        """Player stats from the last match"""
        platform = arez.Platform(platform)
        if platform is None:
            await ctx.send("Wrong platform buster!")
            return
        if player.isdecimal():
            player = await self.api.get_player(player)
        else:
            player_obj = await self.api.search_players(player, platform)
            player = await player_obj[0]
        history = await player.get_match_history()
        last = history[0]
        if last.winner == True:
            winner = "Win"
            color = 0x00ccff
        else:
            winner = "Loss"
            color = 0xee1515
        embed = discord.Embed(color=color, title=f"Match ID: `{last.id}` Played: `{humanize.naturaltime(datetime.utcnow() - last.timestamp)}`")
        embed.set_author(name=f"{player.name}({last.player.platform})")
        if last.champion is not None:
            embed.set_thumbnail(url=last.champion.icon_url)
        else:
            embed.set_thumbnail(url=ctx.author.avatar_url)
        if last.champion is not None:
            champ = last.champion.name
        else:
            champ = 'Unknown'
        items = last.items
        item = '\n'.join(map(str, items))
        cards = '\n'.join(map(str, last.loadout.cards))
        desc = (
            f"**Map Name**: {last.map_name}\n"
            f"**Queue Type**: {last.queue}\n"
            f"**Region**: {last.region}\n"
            f"**Match Stats**: {winner} - {last.score[0]}/{last.score[1]} duration {last.duration.minutes} minutes\n"
            f"**Champion**: {champ}\n"
            f"**Kills/Deaths/Assists**: {last.kda_text} ({last.kda2:.1f})\n"
            f"**Damage**: {last.damage_done}\n"
            f"**Healing**: {last.healing_done}\n"
            f"**Shielding**: {last.shielding}\n"
            f"**Objectice Time**: {last.objective_time}\n"
            f"**Credits Earned**: {last.credits}\n"
            f"**Items Bought**: \n{item}\n"
            f"**Loadout**: {last.loadout.talent}\n{cards}\n"
        )
        embed.description = desc
        #embed.add_field(name="Queue/Map", value=f"{last.queue} - {last.map_name}")
        #embed.add_field(name="Region", value=last.region)
        #embed.add_field(name="Match Stats", value=f"{winner} - {last.score[0]}/{last.score[1]} duration: {last.duration.minutes} minutes")
        #if last.champion is not None:
        #    embed.add_field(name="Champion", value=last.champion.name)
        #else:
        #    embed.add_field(name="Champion", value="Unknown")
        #embed.add_field(name="Kills/Deaths/Assists", value=f"{last.kda_text} ({last.kda2:.1f}) max streak: {last.multikill_max}")
        #embed.add_field(name="Damage", value=last.damage_done)
        #if last.healing_done == 0:
        #   pass
        #else:
        #    embed.add_field(name="Healing", value=last.healing_done)
        #if last.shielding == 0:
       #     pass
       # else:
       #     embed.add_field(name="Shielding", value=last.shielding)
        #embed.add_field(name="Credits", value=last.credits)
        #embed.add_field(name="Objective Time", value=last.objective_time)
       #items = last.items
        #item = '\n'.join(map(str, items))
       # embed.add_field(name="Items Bought", value=f"{item}", inline=False)
       # cards = '\n'.join(map(str, last.loadout.cards))
      #  embed.add_field(name="Loadout", value=f"{last.loadout.talent}\n{cards}", inline=False)
        embed.set_footer(text=f"Played {humanize.naturaltime(datetime.utcnow() - last.timestamp)}")
        #embed.set_footer(text=f"Played: {humanize.naturaltime(datetime.utcnow() - last.timestamp)} time took to execute {(time.time() - start_time)}")
        await ctx.send(embed=embed)
        