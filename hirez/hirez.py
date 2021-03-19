import arez
import discord
import asyncio
import humanize
import pkg_resources
import time
from datetime import datetime
from redbot.core import commands
from tabulate import tabulate
from redbot.core.utils.chat_formatting import pagify
from redbot.core.utils.chat_formatting import box
import discord
from io import BytesIO
from .my_utils import *

class  Hirez(commands.Cog):
    """
    Returns stats for Paladins made by Evil Mojo Studios
    Every command is subject to change and in constant development.
    Version: 0.1.24

    Developed by Mucski
    """
    def __init__(self, bot):
        self.bot = bot
        self.f = open("/home/ubuntu/key.txt", "r")
        self.auth = self.f.readline()
        self.devid = self.f.readline()
        self.api = arez.PaladinsAPI(dev_id=self.devid.strip(), auth_key=self.auth.strip())
       
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
    async def hitest(self, ctx):
        await ctx.send("Your mom")

    @commands.command()
    async def stats(self, ctx, player, platform="pc"):
        """Player stats, title, avatar and more"""
        start_time = time.time()
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
            f"```Account level: {player.level}\n"
            f"Playtime: {int(player.playtime.total_hours())} hours\n"
            f"Region: {player.region}\n"
            f"Champions Owned: {player.champion_count}\n"
            f"Achievements Unlocked: {player.total_achievements}\n"
            f"Account Created: {humanize.naturaltime(datetime.utcnow() - player.created_at)}\n"
            f"Last Login: {humanize.naturaltime(datetime.utcnow() - player.last_login)}\n```"
            "\n\n"
            f"**__Casual Stats__**\n"
            f"```Win Rate: {player.casual.wins} / {player.casual.losses} ({player.casual.winrate_text})\n"
            f"Deserted: {player.casual.leaves}\n```"
            "\n\n"
            f"**__Ranked Stats Season {player.ranked_best.season}__**\n"
            f"```Win Rate: {player.ranked_best.wins} / {player.ranked_best.losses} ({player.ranked_best.winrate_text})\n"
            f"Deserted: {player.ranked_best.leaves}\n"
            f"Ranked Type: {player.ranked_best.type}\n"
            f"Current Rank: {player.ranked_best.rank} ({player.ranked_best.points} TP)\n```"
        )
        embed = discord.Embed(color=await self.bot.get_embed_color(ctx), title=f"{player.name}({player.platform}) _{player.title}_")
        embed.description=desc
        #embed.set_author(name=f"{player.name}({player.platform})")
        embed.set_thumbnail(url=player.avatar_url)
        embed.set_footer(text=f"Fetched in {(time.time() - start_time)}, ID: {player.id}")
        await ctx.send(embed=embed)
        
    @commands.command()
    async def matchimage(self, ctx, player, match_id=None, colored="-b"):
        platform = "pc"
        platform = arez.Platform(platform)
        if platform is None:
            await ctx.send("Wrong platform")
            return
        if player.isdecimal():
            player = await self.api.get_player(player)
        else:
            player_obj = await self.api.search_players(player, platform)
            player = await player_obj[0]
        history = await player.get_match_history()
        last = history[0]
        match = await self.api.get_match(last.id, expand_players=True)
        team1_data = []
        team2_data = []
        team1_champs = []
        team2_champs = []
        team1_parties = {}
        team2_parties = {}
        temp = []
        new_party_id = 0

        # handles if they provide the color option and no match id
        try:
            match_id = int(match_id)
        except BaseException:
            colored = match_id
            match_id = -1

        if match_id == -1 or match_id == last.id:
            match_data = await self.api.get_match(last.id, expand_players=True)
            match_info = [match.winning_team, match.duration, match.region,
                            str(match.map_name).replace("LIVE", ""), match.score[0], match.score[1]]
            # print(match.winStatus, match.matchMinutes, match.matchRegion,
            #      str(match.mapName).replace("LIVE", ""))
            for pd in match_data:
                temp = [pd.bans[0], pd.bans[1], pd.bans[2], pd.bans[3]]
                if pd.taskForce == 1:
                    kda = "{}/{}/{}".format(pd.kills, pd.deaths, pd.assists)
                    team1_data.append([pd.player.name, pd.player.level, "{:,}".format(pd.credits), kda,
                                        "{:,}".format(pd.damage_done), "{:,}".format(pd.damage_taken),
                                        pd.objective_time, "{:,}".format(pd.damage_mitigated),
                                        "{:,}".format(pd.healing_done), pd.player.party_number, pd.player.platform])
                    team1_champs.append(pd.player.champion.name)
                    if pd.player.party_number not in team1_parties or pd.player.party_number == 0:
                        team1_parties[pd.player.party_number] = ""
                    else:
                        if team1_parties[pd.player.party_number] == "":
                            new_party_id += 1
                            team1_parties[pd.player.party_number] = "" + str(new_party_id)
                else:
                    kda = "{}/{}/{}".format(pd.killsPlayer, pd.deaths, pd.assists)
                    team2_data.append([pd.player.name, pd.player.level, "{:,}".format(pd.credits), kda,
                                        "{:,}".format(pd.damage_done), "{:,}".format(pd.damage_taken),
                                        pd.objective_time, "{:,}".format(pd.damage_mitigated),
                                        "{:,}".format(pd.healing_done), pd.player.party_number, pd.player.platform])
                    team2_champs.append(pd.player.champion.name)
                    if pd.partyId not in team2_parties or pd.partyId == 0:
                        team2_parties[pd.player.party_number] = ""
                    else:
                        if team2_parties[pd.player.party_number] == "":
                            new_party_id += 1
                            team1_parties[pd.player.party_number] = "" + str(new_party_id)

            # print("team1: " + str(team1_parties), "team2: " + str(team2_parties))
            color = True if colored == "-c" else False

            buffer = await helper.create_history_image(team1_champs, team2_champs, team1_data, team2_data,
                                                        team1_parties, team2_parties, (match_info + temp), color)

            file = discord.File(filename="TeamMatch.png", fp=buffer)
        await ctx.send(file=file)
        
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
        await ctx.send(embed=e)

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
        e = discord.Embed(color=await self.bot.get_embed_color(ctx), title=f"Current match for {player.name} - _{player.title}_")
        e.set_thumbnail(url=player.avatar_url)
        e.add_field(name="Match", value=f"``{match.id}`` - {match.queue} - {match.map_name} - { match.region}")
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
        status = arez.StatusPage("http://status.hirezstudios.com/")
        csirke = await status.get_status()
        desc = (
            f"**Hirez Infrastructure**: {csirke.status}\n"
            f"**Incident Impact**: {csirke.impact}\n"
            f"**{csirke.component('Paladins PC').name}**: {csirke.component('Paladins PC').status}\n"
            f"**{csirke.component('Paladins PS4').name}**: {csirke.component('Paladins PS4').status}\n"
            f"**{csirke.component('Paladins Xbox').name}**: {csirke.component('Paladins Xbox').status}\n"
            f"**{csirke.component('Paladins Switch').name}**: {csirke.component('Paladins Switch').status}\n"
            f"**{csirke.component('Paladins Epic').name}**: {csirke.component('Paladins Epic').status}\n"
            f"**{csirke.component('Hi-Rez Public APIs').name}**: {csirke.component('Hi-Rez Public APIs').status}\n"
        )
        e = discord.Embed(color=csirke.color, title="Hirez Status", description=desc)
        e.set_footer(text=f"Last updated at: {csirke.updated_at}")
        await ctx.send(embed=e)
    
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
 
        embed.description = desc
        embed.set_footer(text=f"Played {humanize.naturaltime(datetime.utcnow() - last.timestamp)}")
        await ctx.send(embed=embed)