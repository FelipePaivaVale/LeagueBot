import aiohttp
import config.config as config

class RiotAPI:
    def __init__(self):
        self.api_key = config.Config.RIOT_API_KEY
        self.region = config.Config.DEFAULT_REGION
        self.match_region = config.Config.MATCH_REGION
        self.headers = {'X-Riot-Token': self.api_key}

    async def get_summoner_by_name(self, summoner_name):
        url = f'https://{self.region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                print(response)
                if response.status == 200:
                    return await response.json()
                return None

    async def get_summoner_rank(self, summoner_id):
        url = f'https://{self.region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                print(response)
                if response.status == 200:
                    return await response.json()
                return None

    async def get_match_history(self, puuid, count=5):
        url = f'https://{self.match_region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids'
        params = {'count': count}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers, params=params) as response:
                print(response)
                if response.status == 200:
                    return await response.json()
                return None

    async def get_match_details(self, match_id):
        url = f'https://{self.match_region}.api.riotgames.com/lol/match/v5/matches/{match_id}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                print(response)
                if response.status == 200:
                    return await response.json()
                return None