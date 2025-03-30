import nextcord
from nextcord.ext import commands
import config.config as config

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    for cog in ['summoner', 'matches', 'champions']:
        try:
            bot.load_extension(f'cogs.{cog}')
            print(f'Cog {cog} carregado com sucesso')
        except Exception as e:
            print(f'Falha ao carregar cog {cog}: {e}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

if __name__ == '__main__':
    bot.run(config.Config.DISCORD_TOKEN)