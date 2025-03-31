import aiohttp
import config.config as config
from urllib.parse import quote
from utils.helpers import DDragonHelper, QueueHelper

class RiotAPI:
    def __init__(self):
        self.api_key = config.Config.RIOT_API_KEY
        self.region = config.Config.DEFAULT_REGION
        self.match_region = config.Config.MATCH_REGION
        self.headers = {'X-Riot-Token': self.api_key}
        self.queue_helper = QueueHelper()
        self.ddragon = DDragonHelper()

    async def get_current_version(self):
        return await self.ddragon.get_current_version()

    async def get_account_by_riot_id(self, game_name, tag_line):
        """Obtém conta pelo Riot ID (gameName#tagLine)"""
        url = f'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{quote(game_name)}/{quote(tag_line)}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()
                return None

    async def get_summoner_by_puuid(self, puuid):
        """Obtém summoner por PUUID"""
        url = f'https://{self.region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()
                return None

    async def get_summoner_rank(self, summoner_id):
        url = f'https://{self.region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()
                return None

    async def get_match_history(self, puuid, count=5):
        url = f'https://{self.match_region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids'
        params = {'count': count}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers, params=params) as response:
                if response.status == 200:
                    return await response.json()
                return None

    async def get_match_details(self, match_id):
        url = f'https://{self.match_region}.api.riotgames.com/lol/match/v5/matches/{match_id}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()
                return None
            
    async def check_rate_limits(self, response):
        """Verifica os headers de rate limit"""
        limits = {
            'app_limit': response.headers.get('X-App-Rate-Limit'),
            'app_count': response.headers.get('X-App-Rate-Limit-Count'),
            'method_limit': response.headers.get('X-Method-Rate-Limit'),
            'method_count': response.headers.get('X-Method-Rate-Limit-Count')
        }
        print("Rate limits:", limits)

    async def get_champion_data(self, champion_name):
        return await self.ddragon.get_champion_data(champion_name)
    
    async def get_queue_description(self, queue_id):
        """Obtém a descrição amigável de um tipo de fila"""
        return await self.queue_helper.get_queue_description(queue_id)