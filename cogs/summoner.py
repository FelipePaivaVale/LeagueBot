import nextcord
from nextcord.ext import commands
from utils.riot_api import RiotAPI
import asyncio
from utils.riot_api import RiotAPI

class SummonerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.riot_api = RiotAPI()

    @commands.command(name='invocador', aliases=['summoner', 'player'])
    async def summoner_info(self, ctx, *, riot_id):
        if '#' not in riot_id:
            return await ctx.send("Formato incorreto. Use: nome#tag (ex: gambling lover#bet)")

        game_name, tag_line = riot_id.rsplit('#', 1)
        message = await ctx.send(f"🔍 Buscando invocador {game_name}#{tag_line}...")

        try:
            account = await self.riot_api.get_account_by_riot_id(game_name, tag_line)
            if not account:
                return await message.edit(content="❌ Conta não encontrada.")

            summoner = await self.riot_api.get_summoner_by_puuid(account['puuid'])
            if not summoner:
                return await message.edit(content="❌ Invocador não encontrado.")

            ranks = await self.riot_api.get_summoner_rank(summoner['id'])
            profile_icon_url = await self.riot_api.ddragon.get_profile_icon_url(summoner['profileIconId'])

            embed = nextcord.Embed(
                title=f"{account['gameName']}#{account['tagLine']}",
                color=nextcord.Color.blue()
            )
            
            embed.set_thumbnail(url=profile_icon_url)
            embed.add_field(name="Nível", value=summoner['summonerLevel'], inline=True)
            embed.add_field(name="Região", value=self.riot_api.region.upper(), inline=True)
            
            if ranks:
                for rank in ranks:
                    queue_type = self._translate_queue_type(rank['queueType'])
                    winrate = (rank['wins'] / (rank['wins'] + rank['losses'])) * 100
                    embed.add_field(
                        name=queue_type,
                        value=(
                            f"{self._translate_tier(rank['tier'])} {rank['rank']} - {rank['leaguePoints']} LP\n"
                            f"Winrate: {winrate:.1f}% "
                            f"({rank['wins']}W {rank['losses']}L)"
                        ),
                        inline=False
                    )
            else:
                embed.add_field(name="Ranque", value="Não ranqueado", inline=False)
            
            await message.edit(content=None, embed=embed)

        except Exception as e:
            await message.edit(content=f"⚠️ Erro ao buscar informações: {str(e)}")

    async def _get_with_retry(self, api_func, *args):
        """Tenta uma chamada de API com múltiplas tentativas"""
        for attempt in range(self.max_retries):
            try:
                result = await api_func(*args)
                if result or attempt == self.max_retries - 1:
                    return result
                await asyncio.sleep(self.retry_delay)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise e
                await asyncio.sleep(self.retry_delay)

    async def _build_summoner_embed(self, account, summoner, ranks):
        """Constrói o embed de resposta"""
        embed = nextcord.Embed(
            title=f"{account['gameName']}#{account['tagLine']}",
            color=nextcord.Color.blue()
        )
        
        embed.set_thumbnail(
            url=f"https://ddragon.leagueoflegends.com/cdn/{self.riot_api.ddragon_version}/img/profileicon/{summoner['profileIconId']}.png"
        )
        
        embed.add_field(name="Nível", value=summoner['summonerLevel'], inline=True)
        embed.add_field(name="Região", value=self.riot_api.region.upper(), inline=True)
        
        if ranks:
            for rank in ranks:
                queue_type = self._translate_queue_type(rank['queueType'])
                winrate = (rank['wins'] / (rank['wins'] + rank['losses'])) * 100
                embed.add_field(
                    name=queue_type,
                    value=(
                        f"{self._translate_tier(rank['tier'])} {rank['rank']} - {rank['leaguePoints']} LP\n"
                        f"Winrate: {winrate:.1f}% "
                        f"({rank['wins']}W {rank['losses']}L)"
                    ),
                    inline=False
                )
        else:
            embed.add_field(name="Ranque", value="Não ranqueado", inline=False)
            
        return embed

    def _translate_queue_type(self, queue_type):
        translations = {
            'RANKED_SOLO_5x5': 'Ranqueada Solo/Duo',
            'RANKED_FLEX_SR': 'Ranqueada Flex',
            'RANKED_TFT': 'TFT Ranqueado'
        }
        return translations.get(queue_type, queue_type)

    def _translate_tier(self, tier):
        translations = {
            'IRON': 'Ferro',
            'BRONZE': 'Bronze',
            'SILVER': 'Prata',
            'GOLD': 'Ouro',
            'PLATINUM': 'Platina',
            'DIAMOND': 'Diamante',
            'MASTER': 'Mestre',
            'GRANDMASTER': 'Grão-Mestre',
            'CHALLENGER': 'Desafiante'
        }
        return translations.get(tier, tier)

def setup(bot):
    bot.add_cog(SummonerCog(bot))