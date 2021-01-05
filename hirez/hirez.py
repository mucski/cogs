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
from discord import file
#from PIL import Image, ImageFont, ImageDraw, ImageOps
#from io import BytesIO
from .my_utils import *
#import .my_utils as helper

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
    async def hitest(self, ctx):
        for pd in match_data:
            temp = [pd.banName1, pd.banName2, pd.banName3, pd.banName4]
            if pd.taskForce == 1:
                kda = "{}/{}/{}".format(pd.killsPlayer, pd.deaths, pd.assists)
                team1_data.append([pd.playerName, pd.accountLevel, "{:,}".format(pd.goldEarned), kda,
                                   "{:,}".format(pd.damagePlayer), "{:,}".format(pd.damageTaken),
                                   pd.objectiveAssists, "{:,}".format(pd.damageMitigated),
                                   "{:,}".format(pd.healing), pd.partyId, pd.platform])
                team1_champs.append(pd.referenceName)
                if pd.partyId not in team1_parties or pd.partyId == 0:
                    team1_parties[pd.partyId] = ""
                else:
                    if team1_parties[pd.partyId] == "":
                        new_party_id += 1
                        team1_parties[pd.partyId] = "" + str(new_party_id)
            else:
                kda = "{}/{}/{}".format(pd.killsPlayer, pd.deaths, pd.assists)
                team2_data.append([pd.playerName, pd.accountLevel, "{:,}".format(pd.goldEarned), kda,
                                   "{:,}".format(pd.damagePlayer), "{:,}".format(pd.damageTaken),
                                   pd.objectiveAssists, "{:,}".format(pd.damageMitigated),
                                   "{:,}".format(pd.healing), pd.partyId, pd.platform])
                team2_champs.append(pd.referenceName)
                if pd.partyId not in team2_parties or pd.partyId == 0:
                    team2_parties[pd.partyId] = ""
                else:
                    if team2_parties[pd.partyId] == "":
                        new_party_id += 1
                        team2_parties[pd.partyId] = str(new_party_id)

        #team1 = ["Evie", "Maeve", "Fernando", "Sha Lin", "Lex"]
        #team2 = ["Makoa", "Viktor", "Jenos", "Cassie", "Mal Damba"]
        #ranks1 = ["Gold", "Silver", "Bronze", "Bronze", "Unranked"]
        #ranks2 = ["Gold", "Gold", "Master", "GM", "Silver"]
        buffer = await create_history_image(team1champs, team2champs, team1data, team2data, team1parties, team2parties, (match_info + temp), color)
        #sex = await create_match_image(team1, team2, ranks1, ranks2)
        file = discord.File(filename="SuckMe.png", fp=buffer)
        await ctx.send("Fuck you!", file=file)

    @commands.command()
    async def stats(self, ctx, player, platform = "pc"):
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
    async def matchimage(self, ctx, player, platform="pc"):
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
        #match id
        last = history[0]
        match = await self.api.get_match(last.id, expand_players=True)
        match_info = (match.score, match.duration, match.region, match.map_name, match.score[0], match.score[1])
        team1data = []
        team2data = []
        team1champs = []
        team2champs = []
        team1parties = {}
        team2parties = {}
        temp = match.bans
        new_party_id = 0
        for match_player in match.players:
            if match_player.player.private:
                continue
            if match_player.team_number != 1:
                continue
            team1data.append([match_player.player.name, match_player.account_level, match_player.credits, match_player.kda_text,
                             match_player.damage_done, match_player.damage_taken, match_player.objective_time, match_player.damage_mitigated, 
                             match_player.healing_done, match_player.party_number, match_player.player.platform])
            team1champs.append(match_player.champion)
            if match_player.party_number not in team1parties or match_player.party_number == 0:
                team1parties.append("")
            else:
                if team1parties == "":
                    new_party_id += 1
                    team1parties.append(str(new_party_id))
            #players.append(match_player.champion)
            #name = players.append(match_player.player.name)
        for match_player in match.players:
            if match_player.player.private:
                continue
            if match_player.team_number != 2:
                continue
            team2data.append([match_player.player.name, match_player.account_level, match_player.credits, match_player.kda_text,
                             match_player.damage_done, match_player.damage_taken, match_player.objective_time, match_player.damage_mitigated, 
                             match_player.healing_done, match_player.party_number, match_player.player.platform])
            team2champs.append(match_player.champion)
            if match_player.party_number not in team2parties or match_player.party_number == 0:
                team2parties.append("")
            else:
                if team2parties == "":
                    new_party_id += 1
                    team2parties.append(str(new_party_id))
            #players.append(match_player.champion)
        #ranks = []
        #for match_player in match.players:
            #if match_player.player.private:
                #continue
            #ranks.append(match_player.player.ranked_best.rank)
        color = True if Colored == "-c" else False
        buffer = await create_history_image(team1champs, team2champs, team1data, team2data, team1parties, team2parties, (match_info + temp), color)
        file = discord.File(filename="Yourmom.png", fp=buffer)
        await ctx.send(file=file)
        #await ctx.send(team2data)
        
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
        #sex = await match.expand_players(match)
        #await ctx.send(sex)

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