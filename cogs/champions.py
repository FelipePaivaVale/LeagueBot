import nextcord
from nextcord.ext import commands
from utils.riot_api import RiotAPI

class ChampionsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.riot_api = RiotAPI()

    @commands.command(name='campeao', aliases=['champ', 'champion'])
    async def champion_info(self, ctx, *, champion_name):
        message = await ctx.send(f"Buscando informações sobre {champion_name}...")
        
        try:
            champion_data = await self.riot_api.get_champion_data(champion_name.capitalize())
            if not champion_data:
                return await message.edit(content="Campeão não encontrado!")

            champ = champion_data['data'][champion_name.capitalize()]
            champion_icon = await self.riot_api.ddragon.get_champion_icon_url(champ['image']['full'].replace('.png', ''))
            
            embed = nextcord.Embed(
                title=f"{champ['name']} - {champ['title']}",
                description=champ['blurb'],
                color=nextcord.Color.gold()
            )
            
            embed.set_thumbnail(url=champion_icon)
            
            embed.add_field(
                name="Informações Básicas",
                value=(
                    f"**Classe**: {', '.join(champ['tags'])}\n"
                    f"**Dificuldade**: {champ['info']['difficulty']}/10\n"
                    f"**HP**: {champ['stats']['hp']} (+{champ['stats']['hpperlevel']})\n"
                    f"**Dano**: {champ['stats']['attackdamage']} (+{champ['stats']['attackdamageperlevel']})"
                ),
                inline=True
            )
            
            await message.edit(content=None, embed=embed)

        except Exception as e:
            await message.edit(content=f"Erro ao buscar campeão: {str(e)}")

def setup(bot):
    bot.add_cog(ChampionsCog(bot))