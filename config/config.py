import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    RIOT_API_KEY = os.getenv('RIOT_API_KEY')
    DEFAULT_REGION = 'br1'
    MATCH_REGION = 'americas'
    DDRAGON_VERSION = '15.6.1'
    MAX_MATCHES = 5