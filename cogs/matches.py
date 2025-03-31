import nextcord
from nextcord.ext import commands
from utils.riot_api import RiotAPI

class MatchesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.riot_api = RiotAPI()

    @commands.command(name='partidas', aliases=['matches', 'historico'])
    async def match_history(self, ctx, *, riot_id, match_count: int = 5):
        """Mostra as últimas partidas usando Riot ID (nome#tag)"""
        if '#' not in riot_id:
            return await ctx.send("Formato incorreto. Use: nome#tag (ex: gambling lover#bet)")

        game_name, tag_line = riot_id.rsplit('#', 1)
        message = await ctx.send(f"Buscando partidas de {game_name}#{tag_line}...")

        # Obtém a conta primeiro
        account = await self.riot_api.get_account_by_riot_id(game_name, tag_line)
        if not account:
            return await message.edit(content="Conta não encontrada.")

        # Obtém as partidas
        match_ids = await self.riot_api.get_match_history(account['puuid'], match_count)
        if not match_ids:
            return await message.edit(content="Nenhuma partida recente encontrada.")
        
        embed = nextcord.Embed(
            title=f"Últimas {len(match_ids)} partidas de {account['gameName']}#{account['tagLine']}",
            color=nextcord.Color.purple()
        )
        
        for match_id in match_ids[:5]:
            match = await self.riot_api.get_match_details(match_id)
            if match:
                participant = next(
                    p for p in match['info']['participants'] 
                    if p['puuid'] == account['puuid']
                )
                
                # Formatação melhorada
                embed.add_field(
                    name=f"{participant['championName']} - {self._format_queue(match['info']['queueId'])}",
                    value=(
                        f"**KDA**: {participant['kills']}/{participant['deaths']}/{participant['assists']} "
                        f"(Ratio: {(participant['kills']+participant['assists'])/max(1, participant['deaths']):.1f})\n"
                        f"**Resultado**: {'🏆 Vitória' if participant['win'] else '💀 Derrota'}\n"
                        f"**Duração**: {match['info']['gameDuration']//60}m {match['info']['gameDuration']%60}s\n"
                        f"**Modo**: {match['info']['gameMode']}"
                    ),
                    inline=False
                )
        
        await message.edit(content=None, embed=embed)

    def _format_queue(self, queue_id):
        queues = {
            420: "Solo/Duo",
            440: "Flex",
            450: "ARAM",
            900: "URF"
        }
        return queues.get(queue_id, f"Queue {queue_id}")

def setup(bot):
    bot.add_cog(MatchesCog(bot))