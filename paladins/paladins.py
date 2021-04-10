import arez
from redbot.core import checks, commands
import asyncio
import humanize
from datetime import datetime
import discord
from discord import File
from .helper import helper
from redbot.core.utils.chat_formatting import pagify
import aiohttp
import json
from io import StringIO
import math
from tabulate import tabulate
from typing import Union

class Paladins(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.f = open("/home/ubuntu/key.txt", "r")
        self.auth = self.f.readline()
        self.devid = self.f.readline()
        self.api = arez.PaladinsAPI(dev_id=self.devid.strip(),
                                    auth_key=self.auth.strip())

    def cog_unload(self):
        asyncio.createTask(self.api.close())
        self.f.close()
        
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            exc = error.original
            if isinstance(exc, arez.Unavailable):
                await ctx.send("```\nHiRez API is unavailable.\n```")
                return
            if isinstance(exc, arez.Private):
                await ctx.send("```\nRequested profile is set to private\n```")
                return
            if isinstance(exc, arez.NotFound):
                await ctx.send("```\nNot found!\n```")
                return
        await ctx.bot.on_command_error(ctx, error, unhandled_by_cog=True)

    @commands.command()
    async def match(self, ctx, matchid: int):
        """
        Returns a match played from a given ID.
        This command only supports integer. 
        For player names use `[p]last (player) (platform)` 
        See `[p]help last` for more info.
        """
        async with ctx.typing():
            match = await self.api.get_match(matchid, expand_players=True)
            team1_data = []
            team2_data = []
            team1_champs = []
            team1_ranks = []
            team2_ranks = []
            team2_champs = []
            match_info = [match.winning_team, match.duration.minutes, match.region.name,
                          match.map_name, match.score[0], match.score[1]]
            temp = match.bans
            for match_player in match.players:
                row = [
                        match_player.player.name, match_player.account_level, match_player.credits, match_player.kda_text,
                        match_player.damage_done, match_player.damage_taken, match_player.objective_time, match_player.damage_mitigated,
                        match_player.healing_done, match_player.party_number, match_player.player.platform, match_player.healing_self,
                        match_player.kda
                ]
                if match_player.team_number == 1:
                    if match_player.player.private:
                        rank = "99"
                    else:
                        rank = match_player.player.ranked_best.rank.value
                    team1_data.append(row)
                    team1_champs.append(match_player.champion.name)
                    team1_ranks.append(rank)
                else:
                    if match_player.player.private:
                        rank = "99"
                    else:
                        rank = match_player.player.ranked_best.rank.value
                    team2_data.append(row)
                    team2_champs.append(match_player.champion.name)
                    team2_ranks.append(rank)
            buffer = await helper.history_image(team1_champs, team2_champs, team1_data, team2_data, team1_ranks,
                                                team2_ranks, (match_info + temp))
            file = discord.File(filename=f"{matchid}.png", fp=buffer)
        await ctx.send(file=file)
        
    @commands.command()
    @checks.is_owner()
    async def proto(self, ctx):
        async with ctx.typing():
            team1_data = []
            team2_data = []
            team1_champs = []
            team1_ranks = []
            team2_ranks = []
            team2_champs = []
            cunt = 0
            match_info = ["1", "30", "Japan",
                          "Timber Mill", "1", "4"]
            temp = ["Makoa", "Yagorath", "Furia", "Jenos"]
            while cunt < 10:
                cunt += 1
                row = [
                        "TestSomeLongName", "999", "9999", "99/0/99",
                        "999999", "999999", "999", "999999",
                        "999999", "0", "Steam", "999999",
                        9.99
                ]
                if cunt < 6:
                    rank = "22"
                    team1_data.append(row)
                    team1_champs.append("Octavia")
                    team1_ranks.append(rank)
                else:
                    rank = "22"
                    team2_data.append(row)
                    team2_champs.append("Yagorath")
                    team2_ranks.append(rank)
            buffer = await helper.history_image(team1_champs, team2_champs, team1_data, team2_data, team1_ranks,
                                                team2_ranks, (match_info + temp))
            file = discord.File(filename=f"prototype.png", fp=buffer)
        await ctx.send(file=file)
            

    @commands.command()
    async def last(self, ctx, player: Union[discord.Member, str] = None, platform="PC"):
        """
        Returns the last played match by `player`
        `player` can be a string or a discord member (mention)
        Platform is optional
        If you have Discord linked to HiRez, you can just type `[p]last`
        followed by nothing.
        """
        async with ctx.typing():
            if isinstance(player, discord.Member) or player is None:
                if player is None:
                    # use the ID of the caller
                    discord_id = ctx.author.id
                else:
                    # use the ID of the person mentioned
                    discord_id = player.id
                    # use discord_id to lookup their profile
                try:
                    player = await self.api.get_from_platform(discord_id, arez.Platform.Discord)
                except arez.NotFound:
                    await ctx.send("```\nDiscord account not linked to HiRez. Please link it first\n```")
                    return
            else:
                # player is a str here
                try:
                    player_list = await self.api.search_players(player, arez.Platform(platform))
                except arez.NotFound:
                    await ctx.send("```\nNo players found with that name\n```")
                    return
                player = player_list[0]
            match_list = await player.get_match_history()
            if not match_list:
                await ctx.send("```\nNo recent matches found.\n```")
                return
            match = await match_list[0]
            await match.expand_players()
            team1_data = []
            team2_data = []
            team1_champs = []
            team1_ranks = []
            team2_ranks = []
            team2_champs = []
            match_info = [match.winning_team, match.duration.minutes, match.region.name,
                          match.map_name, match.score[0], match.score[1]]
            temp = match.bans
            for match_player in match.players:
                row = [
                        match_player.player.name, match_player.account_level, match_player.credits, match_player.kda_text,
                        match_player.damage_done, match_player.damage_taken, match_player.objective_time, match_player.damage_mitigated,
                        match_player.healing_done, match_player.party_number, match_player.player.platform, match_player.healing_self,
                        match_player.kda
                ]
                if match_player.team_number == 1:
                    if match_player.player.private:
                        rank = "99"
                    else:
                        rank = match_player.player.ranked_best.rank.value
                    team1_data.append(row)
                    team1_champs.append(match_player.champion.name)
                    team1_ranks.append(rank)
                else:
                    if match_player.player.private:
                        rank = "99"
                    else:
                        rank = match_player.player.ranked_best.rank.value
                    team2_data.append(row)
                    team2_champs.append(match_player.champion.name)
                    team2_ranks.append(rank)
            buffer = await helper.history_image(team1_champs, team2_champs, team1_data, team2_data, team1_ranks,
                                                team2_ranks, (match_info + temp))
            file = discord.File(filename=f"{player}.png", fp=buffer)
        await ctx.send(file=file)

    @commands.command()
    @checks.is_owner()
    async def hirez(self, ctx, request, *msg):
        try:
            data = await self.api.request(request, *msg)
        except arez.HTTPException as exc:
            exc = exc.cause
            if isinstance(exc, aiohttp.ClientResponseError):
                await ctx.send(f"```\n{exc.status}: {exc.message}\n```")
                return
            elif isinstance(exc, aiohttp.ClientConnectionError):
                await ctx.send(f"```\nFailed to connect to api.\n```")
                return
            elif isinstance(exc, asyncio.TimeoutError):
                await ctx.send("```\nTimed out.\n```")
                return
            else:
                await ctx.send("```\nUnknown error\n```")
                return
        response = json.dumps(data, indent=4, sort_keys=True)
        if len(response) > 2000:
            f = StringIO(response)
            f.seek(0)
            file = discord.File(filename="output.txt", fp=f)
            await ctx.send(file=file)
        else:
            await ctx.send("```json\n" + response + "```")

    @commands.command()
    @checks.is_owner()
    async def testing(self, ctx, player: Union[discord.Member, str] = None, platform="PC"):
        if isinstance(player, discord.Member) or player is None:
            if player is None:
                # use the ID of the caller
                discord_id = ctx.author.id
            else:
                # use the ID of the person mentioned
                discord_id = player.id
            # use discord_id to lookup their profile
            ret = await self.api.get_from_platform(discord_id, arez.Platform.Discord)
        else:
            # player is a str here
            ret = await self.api.search_players(player, arez.Platform(platform))
            ret = ret[0]
        player = await ret
        await ctx.send(player.name)
        
    @commands.command()
    async def champstats(self, ctx, champion_name = "all", player: Union[discord.Member, str] = None, platform = "PC"):
        """
        `[p]champstats all (player) (platform)` returns a list of every champion.
        `[p]champstats (champion) (player) (platform)` returns a specific champion stats.
        Platform is required for consoles.
        No `player` or `platform` required if linked Discord with HiRez
        """
        async with ctx.typing():
            if isinstance(player, discord.Member) or player is None:
                if player is None:
                    # use the ID of the caller
                    discord_id = ctx.author.id
                    player_name = ctx.author.display_name
                else:
                    # use the ID of the person mentioned
                    discord_id = player.id
                    player_name = player.display_name
                    # use discord_id to lookup their profile
                ret = await self.api.get_from_platform(discord_id, arez.Platform.Discord)
            else:
                # player is a str here
                ret = await self.api.search_players(player, arez.Platform(platform))
                ret = await ret[0]
                player_name = ret.name
            champions_stats = await ret.get_champion_stats()
            stats_dict = {s.champion: s for s in champions_stats}  # Dict[Champion, ChampionStats]
            if champion_name == "all":
                table = []
                for i in range(len(champions_stats)):
                    # table = [["fuck"], ["shit"], ["dick"], ["cunt"]]
                    t = []
                    t.append(f"{champions_stats[i].champion.name}({champions_stats[i].level})")
                    t.append(f"{champions_stats[i].kda}")
                    t.append(f"{champions_stats[i].winrate_text}") 
                    t.append(f"{math.floor(champions_stats[i].playtime.total_hours())} h")
                    table.append(t)
                table_done = tabulate(table, headers=["Name(lvl)", "K/D/A", "Winrate", "Playtime"], tablefmt="presto")
                for page in pagify(table_done):
                    await ctx.send("```\n{}\n```".format(page))
            else:
                entry = await self.api.get_champion_info()
                champ = entry.champions.get(champion_name)
                if champ is None:
                    await ctx.send("```\nYou dun fucked up the champ's name!\n```")
                    return
                stats = stats_dict.get(champ)
                if stats is None:
                    await ctx.send("```\nYou ain't played this champ yet!\n```")
                    return
                desc = (
                    f"```\nChampion role: {champ.role}\n"
                    f"Champion level: {stats.level}\n"
                    f"Winrate: {stats.kda_text} ({stats.winrate_text})\n"
                    f"Matches played: {stats.matches_played}\n"
                    f"Playtime: {math.floor(stats.playtime.total_hours())} hours\n"
                    f"Experience: {stats.experience}\n"
                    f"Last played: {humanize.naturaltime(datetime.utcnow() - stats.last_played)}\n```"
                )
                e = discord.Embed(color=await self.bot.get_embed_color(ctx), title=f"{champ.name} ({champ.title})")
                e.set_thumbnail(url=champ.icon_url)
                e.description = desc
                e.set_footer(text=f"Individual champion stats for {player_name}")
                await ctx.send(embed=e)
            
    @commands.command()
    async def stats(self, ctx, name: Union[discord.Member, str] = None, platform="PC"):
        if isinstance(name, discord.Member) or name is None:
            if name is None:
                # use the ID of the caller
                player = ctx.author.id
            else:
                # use the ID of the person mentioned
                player = name.id
                # use discord_id to lookup their profile
            try:
                player_obj = await self.api.get_from_platform(player, arez.Platform.Discord)
            except arez.NotFound:
                await ctx.send("```\nDiscord account not linked to HiRez. Please link it first\n```")
                return
            player = await player_obj
        else:
            # player is a str here
            player_list = await self.api.search_players(name, arez.Platform(platform))
            player = await player_list[0]
        try:
            special = await helper.get_global_kda(player.name)
            special = special[3]
        except asyncio.TimeoutError:
            special = "KDA api down."
        desc = (
            "**__Player Stats__**\n"
            f"```\nAccount level: {player.level}\n"
            f"Playtime: {math.floor(player.playtime.total_hours())} hours\n"
            f"Region: {player.region}\n"
            f"Champions Owned: {player.champion_count}\n"
            f"Achievements Unlocked: {player.total_achievements}\n"
            f"Account Created: "
            f"{humanize.naturaltime(datetime.utcnow() - player.created_at)}\n"
            f"Last Login: "
            f"{humanize.naturaltime(datetime.utcnow() - player.last_login)}\n"
            "```"
            f"**__Casual Stats__**\n"
            f"```\nWin Rate: "
            f"{player.casual.wins}/{player.casual.losses}"
            f" ({player.casual.winrate_text})\n"
            f"KDA: {special}\n"
            f"Deserted: {player.casual.leaves}\n```"
            f"**__Ranked Stats Season {player.ranked_best.season}__**\n"
            f"```\nWin Rate: "
            f"{player.ranked_best.wins}/{player.ranked_best.losses}"
            f" ({player.ranked_best.winrate_text})\n"
            f"Deserted: {player.ranked_best.leaves}\n"
            f"Ranked Type: {player.ranked_best.type}\n"
            f"Current Rank: {player.ranked_best.rank}"
            f" ({player.ranked_best.points} TP)\n```"
        )
        e = discord.Embed(color=await self.bot.get_embed_color(ctx),
                          title=f"{player.name} ({player.platform}) "
                                f"_({player.title})_")
        e.description = desc
        e.set_thumbnail(url=player.avatar_url)
        e.set_footer(text=f"Player ID: {player.id}")
        await ctx.send(embed=e)
