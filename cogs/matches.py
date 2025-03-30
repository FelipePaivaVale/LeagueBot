import nextcord
from nextcord.ext import commands
from utils.riot_api import RiotAPI

class MatchesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.riot_api = RiotAPI()

    @commands.command(name='partidas', aliases=['matches', 'historico'])
    async def match_history(self, ctx, summoner_name, match_count: int = 5):
        """Mostra as últimas partidas - !partidas [nome] [quantidade?]"""
        message = await ctx.send("Buscando histórico de partidas...")
        
        summoner = await self.riot_api.get_summoner_by_name(summoner_name)
        if not summoner:
            return await message.edit(content="Invocador não encontrado!")
        
        match_ids = await self.riot_api.get_match_history(summoner['puuid'], match_count)
        if not match_ids:
            return await message.edit(content="Nenhuma partida recente encontrada!")
        
        embed = nextcord.Embed(
            title=f"Últimas {len(match_ids)} partidas de {summoner['name']}",
            color=nextcord.Color.purple()
        )
        
        for match_id in match_ids[:5]:  # Limitar a 5 para evitar excesso
            match = await self.riot_api.get_match_details(match_id)
            if match:
                participant = next(
                    p for p in match['info']['participants'] 
                    if p['puuid'] == summoner['puuid']
                )
                result = "Vitória" if participant['win'] else "Derrota"
                embed.add_field(
                    name=f"Partida {match_id[:8]}...",
                    value=f"Campeão: {participant['championName']}\n"
                          f"KDA: {participant['kills']}/{participant['deaths']}/{participant['assists']}\n"
                          f"Resultado: {result}",
                    inline=True
                )
        await message.edit(content=None, embed=embed)

def setup(bot):
    bot.add_cog(MatchesCog(bot))