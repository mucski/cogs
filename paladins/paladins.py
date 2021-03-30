import arez
from redbot.core import commands
import asyncio
import humanize
from datetime import datetime
import discord
from discord import File
from .helper import helper


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
                await ctx.send("HiRez API is offline or unavaiable.")
                return
            if isinstance(exc, arez.Private):
                await ctx.send("Requested profile is set to private")
                return
            if isinstance(exc, arez.NotFound):
                await ctx.send("Player was not found")
                return
        await ctx.bot.on_command_error(ctx, error, unhandled_by_cog=True)


    @commands.command()
    async def match(self, ctx, matchId):
        async with ctx.typing():
            try:
                match = await self.api.get_match(int(matchId), expand_players=True)
            except ValueError:
                match = await self.api.get_player(matchId)
                match = await match.get_match_history()
                try:
                    match = await match[0]
                except IndexError:
                    await ctx.send("No match found.")
                    return
            team1_data = []
            team2_data = []
            team1_champs = []
            team1_ranks = []
            team2_ranks = []
            team2_champs = []
            team1_parties = {}
            team2_parties = {}
            # temp = []
            new_party_id = 0
            match_info = [match.winning_team, match.duration.minutes, match.region.name,
                              match.map_name, match.score[0], match.score[1]]
            temp = match.bans
            for player in match.players:
                if player.team_number == 1:
                    if player.player.private:
                        rank = "0"
                    else:
                        gugu = await player.player
                        rank = gugu.ranked_best.rank.value
                    team1_data.append([player.player.name, player.account_level, player.credits, player.kda_text,
                                       player.damage_done, player.damage_taken,
                                       player.objective_time, player.damage_mitigated,
                                       player.healing_done, player.party_number, player.player.platform, player.healing_self])
                    team1_champs.append(player.champion.name)
                    team1_ranks.append(rank)
                    if player.party_number not in team1_parties or player.party_number == 0:
                        team1_parties[player.party_number] = ""
                    else:
                        if team1_parties[player.party_number] == "":
                            new_party_id += 1
                            team1_parties[player.party_number] = "" + str(new_party_id)
                else:
                    if player.player.private:
                        rank = "0"
                    else:
                        gugu = await player.player
                        rank = gugu.ranked_best.rank.value
                    team2_data.append([player.player.name, player.account_level, player.credits, player.kda_text,
                                       player.damage_done, player.damage_taken,
                                       player.objective_time, player.damage_mitigated,
                                       player.healing_done, player.party_number, player.player.platform, player.healing_self])
                    team2_champs.append(player.champion.name)
                    team2_ranks.append(rank)
                    if player.party_number not in team2_parties or player.party_number == 0:
                        team2_parties[player.party_number] = ""
                    else:
                        if team2_parties[player.party_number] == "":
                            new_party_id += 1
                            team2_parties[player.party_number] = "" + str(new_party_id)
            buffer = await helper.history_image(team1_champs, team2_champs, team1_data, team2_data, team1_ranks,
                                                                   team2_ranks, team1_parties, team2_parties, (match_info + temp))
            file = discord.File(filename=f"{matchId}.png", fp=buffer)
        await ctx.send(file=file)


    @commands.command()
    async def datausage(self, ctx):
        data = arez.Endpoint.request(getdataused)
        await ctx.send(f"```json {data} ```")


    @commands.command()
    async def stats(self, ctx, player, platform="PC"):
        platform = arez.Platform(platform)
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
            f"Account Created: "
            f"{humanize.naturaltime(datetime.utcnow() - player.created_at)}\n"
            f"Last Login: "
            f"{humanize.naturaltime(datetime.utcnow() - player.last_login)}\n"
            "```\n\n"
            f"**__Casual Stats__**\n"
            f"```Win Rate: "
            f"{player.casual.wins}/{player.casual.losses}"
            f" ({player.casual.winrate_text})\n"
            f"Deserted: {player.casual.leaves}\n```"
            "\n\n"
            f"**__Ranked Stats Season {player.ranked_best.season}__**\n"
            f"```Win Rate: "
            f"{player.ranked_best.wins}/{player.ranked_best.losses}"
            f" ({player.ranked_best.winrate_text})\n"
            f"Deserted: {player.ranked_best.leaves}\n"
            f"Ranked Type: {player.ranked_best.type}\n"
            f"Current Rank: {player.ranked_best.rank}"
            f" ({player.ranked_best.points} TP)\n```"
        )
        e = discord.Embed(color=await self.bot.get_embed_color(ctx),
                          title=f"{player.name}({player.platform})"
                                f"_({player.title})_")
        e.description = desc
        e.set_thumbnail(url=player.avatar_url)
        e.set_footer(text=f"Player ID: {player.id}")
        await ctx.send(embed=e)
