import nextcord
from nextcord.ext import commands
from utils.riot_api import RiotAPI

class MatchesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.riot_api = RiotAPI()

    @commands.command(name='partidas', aliases=['matches', 'historico'])
    async def match_history(self, ctx, *, riot_id, match_count: int = 5):
        """Mostra as últimas partidas - !partidas nome#tag [quantidade?]"""
        if '#' not in riot_id:
            return await ctx.send("Formato incorreto. Use: nome#tag (ex: gambling lover#bet)")

        game_name, tag_line = riot_id.rsplit('#', 1)
        message = await ctx.send(f"Buscando partidas de {game_name}#{tag_line}...")

        try:
            account = await self.riot_api.get_account_by_riot_id(game_name, tag_line)
            if not account:
                return await message.edit(content="Conta não encontrada.")

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
                    
                    queue_description = await self.riot_api.get_queue_description(match['info']['queueId'])
                    kda_ratio = (participant['kills'] + participant['assists']) / max(1, participant['deaths'])
                    
                    embed.add_field(
                        name=f"{participant['championName']} | {queue_description}",
                        value=(
                            f"**KDA**: {participant['kills']}/{participant['deaths']}/{participant['assists']} "
                            f"(Ratio: {kda_ratio:.2f})\n"
                            f"**Resultado**: {'🏆 Vitória' if participant['win'] else '💀 Derrota'}\n"
                            f"**Duração**: {self._format_duration(match['info']['gameDuration'])}\n"
                            f"**Data**: {self._format_date(match['info']['gameCreation'])}"
                        ),
                        inline=False
                    )
            
            await message.edit(content=None, embed=embed)

        except Exception as e:
            await message.edit(content=f"Erro ao buscar partidas: {str(e)}")

    def _format_duration(self, seconds):
        """Formata a duração da partida em minutos:segundos"""
        mins, secs = divmod(seconds, 60)
        return f"{mins}m {secs}s"

    def _format_date(self, timestamp):
        """Formata o timestamp para data legível"""
        from datetime import datetime
        return datetime.fromtimestamp(timestamp/1000).strftime('%d/%m/%Y %H:%M')

def setup(bot):
    bot.add_cog(MatchesCog(bot))