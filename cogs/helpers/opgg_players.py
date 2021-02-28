import aiohttp
from datetime import datetime
import asyncio

from bs4 import BeautifulSoup as bs
from discord.ext import commands


class Opgg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.url_prefix = "https://"
        self.op_gg_page_ladder_url = "op.gg/ranking/ladder/page="
        self.op_gg_profile_page = "op.gg/summoner/userName="
        self.start_page = 1
        self.regions = ["jp.", "www.", ] # "euw.", "eune.", "na.", "br.", "ru."
        self.rank_to_find = "Gold 2"
        self.rank_ladder = ["Bronze", "Iron", "Silver", "Gold", "Platinum",
                            "Diamond", "Master", "Grandmaster", "Challenger"]
        self.division = "Gold"
        self.division_spot = "2"
        self.total_pages = 0
        self.player_dict = dict()
        self.current_page = 0
        self.final_active_players = {}

    async def request(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return await resp.text()

    async def pages_to_move(self, perc):
        pages_to_move, bla = divmod(self.current_page * perc, 1)
        return pages_to_move

    async def check_player(self, player_rank, region, return_pages=True):
        p_division_spot = player_rank.split(" ")[1]
        p_division = player_rank.split(" ")[0]
        # print(p_division, p_division_spot, "test for nonexistent")

        # print(p_division, p_ladder_spot)
        if player_rank == self.rank_to_find:
            return True
        else:
            # If division matches - start checking if ladder spot is the one we need
            if self.division == p_division:
                # Needed ladder spot > given ladder spot - return +10 pages
                if int(self.division_spot) > int(p_division_spot):
                    return await self.pages_to_move(0.2) if return_pages else False
                # Needed ladder spot < given ladder spot - return -10 pages
                elif int(self.division_spot) < int(p_division_spot):
                    return -(await self.pages_to_move(0.2)) if return_pages else False
            # If division is not equal to what I have - find out if it's lower or higher than we need
            else:
                if self.rank_ladder.index(self.division) > self.rank_ladder.index(p_division):
                    return -(await self.pages_to_move(0.5)) if return_pages else False
                elif self.rank_ladder.index(self.division) < self.rank_ladder.index(p_division):
                    return await self.pages_to_move(0.5) if return_pages else False
                # Check division in accordance to rank ladder index
                # if it's above - go some pages lower

    async def check_if_no_table(self, region, page):
        url = f"{self.url_prefix}{region if region else ''}{self.op_gg_page_ladder_url}{page}"
        response = await self.request(url)

        parser = bs(response, features='lxml')

        error = parser.find('div', {"class": "ErrorMessage"})
        if error:
            print(error)
            print("Nothing in page.")
            return True
        return False

    async def find_players_in_table(self, player):
        player_name = player.find('td', {'class': 'ranking-table__cell ranking-table__cell--summoner'})
        player_rank = player.find('td', {'class': 'ranking-table__cell ranking-table__cell--tier'})
        player_name = player_name.text
        player_rank = player_rank.text.strip()

        return player_name, player_rank

    async def get_players_from_ladder_page(self, page_to_search_in, region, return_if_suitable=False):
        url = f"{self.url_prefix}{region if region else ''}{self.op_gg_page_ladder_url}{page_to_search_in}"
        response = await self.request(url)

        if await self.check_if_no_table(region, page_to_search_in):
            pages_to_move, nesveikas_skaicius = divmod(self.total_pages * 0.4, 1)
            return [], -(pages_to_move)

        parser = bs(response, features='lxml')

        found_players = []
        players = parser.find_all('tr', {"class": 'ranking-table__row'})
        print(239, url)
        for idx, player in enumerate(players, 1):
            player_name, player_rank = await self.find_players_in_table(player)

            # Return True or False if page is correct
            correct_page = await self.check_player(player_rank, region, return_pages=False)
            if not correct_page:
                print(21)
                pages_to_shift = await self.check_player(player_rank, region, return_pages=True)
                if return_if_suitable:
                    return [], pages_to_shift
                return pages_to_shift
            else:
                # print(player_name, player_rank, "needed")
                found_players.append([player_name, player_rank])


            # if idx == 100 or any(player_needed == x for x in [500, -500, 200, -200]):
            #     print(3)
            #     return [], player_needed

        return found_players, 0

    async def find_ladder_middle(self, region):
        url = f"{self.url_prefix}{region if region else ''}{self.op_gg_page_ladder_url}1"
        response = await self.request(url)

        parser = bs(response, features='lxml')

        total_players = parser.find('div', {'class': 'ranking-pagination__desc'})
        total_players = total_players.text.strip().split('Total')[1].split('Summoners')[0].strip().replace(',', '')
        total_players = int(total_players)

        total_pages = int(round(total_players / 100, 0))
        pages_to_move = total_pages * 0.1

        return total_players, total_pages, pages_to_move

    async def find_suitable_table_page(self, region):
        pages_to_change = 0

        while True:
            if self.current_page == self.total_pages:
                print(f"Scanning '{region if region != 'www.' else 'kr.'}' region...")

            self.current_page += pages_to_change

            # url = f"{self.url_prefix}{region if region else ''}{self.op_gg_page_ladder_url}{page}"
            # response = await self.request(url)
            found_players, pages_to_change = await self.get_players_from_ladder_page(self.current_page, region,
                                                                                     return_if_suitable=True)

            if len(found_players) > 1:
                return self.current_page
            else:
                print(f"Shifting pages {pages_to_change}.. Currently on {self.current_page} - "
                      f"'{region if region != 'www.' else 'kr.'}'")

            await asyncio.sleep(0.5)

    async def find_active_player_in_region(self):
        for region, players in self.player_dict.items():
            for player in players:
                player, rank = player
                url = f"{self.url_prefix}{region if region else ''}{self.op_gg_profile_page}"
                url += player

                resp = await self.request(url)
                parser = bs(resp, features="lxml")
                games = parser.find_all('div', {'class': 'GameItemWrap'})
                for game in games:
                    game_type = game.find('div', {'class': 'GameType'}).text.lower()
                    played_ago = game.find('div', {'class': 'TimeStamp'})
                    played_ago = played_ago.findChildren('span')[0]['data-datetime']
                    played_ago = datetime.fromtimestamp(int(played_ago))
                    played_ago = datetime.now() - played_ago

                    if 'solo' in game_type and played_ago.days <= 5:
                        self.final_active_players[region] = player
                        break

                if region in self.final_active_players:
                    break

        return self.final_active_players

    async def get_players(self):
        for region in self.regions:
            total_players, total_pages, pages_to_move = await self.find_ladder_middle(region)
            self.total_pages = total_pages
            self.current_page = self.total_pages / 2

            self.player_dict[region] = []

            page_for_suitable_players = await self.find_suitable_table_page(region)

            found_players, pages_to_change = await self.get_players_from_ladder_page(page_for_suitable_players, region)
            self.player_dict[region] = found_players

        return await self.find_active_player_in_region()

    @commands.command(name='seed')
    async def seed_players(self, ctx):
        string = ""
        op_gg_url = "op.gg/summoner/userName="
        active_players = await self.get_players()
        for region, player in active_players.items():
            string += f"\n[{region}](https://{region}{op_gg_url}{player})"

        await ctx.send(f"```\n{string}\n```")


def setup(bot):
    bot.add_cog(Opgg(bot))
