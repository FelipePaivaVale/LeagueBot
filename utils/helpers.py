import aiohttp
import json
from datetime import datetime, timedelta
import config.config as config

class DDragonHelper:
    _instance = None
    _last_updated = None
    _versions = None
    _current_version = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DDragonHelper, cls).__new__(cls)
        return cls._instance

    async def get_current_version(self):
        """Obtém a versão mais recente do Data Dragon com cache de 1 hora"""
        if (self._last_updated and 
            datetime.now() - self._last_updated < timedelta(hours=1) and 
            self._current_version):
            return self._current_version

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://ddragon.leagueoflegends.com/api/versions.json') as response:
                    if response.status == 200:
                        versions = await response.json()
                        self._versions = versions
                        self._current_version = versions[0]
                        self._last_updated = datetime.now()
                        return self._current_version
        except Exception as e:
            print(f"Erro ao obter versões: {e}")

        return config.Config.DDRAGON_VERSION

    async def get_champion_icon_url(self, champion_name):
        """Retorna a URL do ícone do campeão"""
        version = await self.get_current_version()
        return f'https://ddragon.leagueoflegends.com/cdn/{version}/img/champion/{champion_name}.png'

    async def get_profile_icon_url(self, icon_id):
        """Retorna a URL do ícone de perfil"""
        version = await self.get_current_version()
        return f'https://ddragon.leagueoflegends.com/cdn/{version}/img/profileicon/{icon_id}.png'

    async def get_champion_data(self, champion_name):
        """Obtém dados completos de um campeão"""
        version = await self.get_current_version()
        url = f'https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion/{champion_name}.json'
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        return await response.json()
        except Exception as e:
            print(f"Erro ao obter dados do campeão: {e}")
        return None