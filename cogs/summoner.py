import nextcord
from nextcord.ext import commands
from utils.riot_api import RiotAPI

class SummonerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.riot_api = RiotAPI()

    @commands.command(name='invocador', aliases=['summoner', 'player'])
    async def summoner_info(self, ctx, *, summoner_name):
        """Mostra informações de um invocador - !invocador [nome]"""
        message = await ctx.send("Buscando informações do invocador...")
        
        summoner = await self.riot_api.get_summoner_by_name(summoner_name)
        if not summoner:
            return await message.edit(content="Invocador não encontrado!")
        
        ranks = await self.riot_api.get_summoner_rank(summoner['id'])
        
        embed = nextcord.Embed(
            title=f"Informações de {summoner['name']}",
            color=nextcord.Color.blue()
        )
        embed.set_thumbnail(url=f"https://ddragon.leagueoflegends.com/cdn/13.1.1/img/profileicon/{summoner['profileIconId']}.png")
        embed.add_field(name="Nível", value=summoner['summonerLevel'], inline=True)
        
        if ranks:
            for rank in ranks:
                queue_type = 'Ranqueada Solo/Duo' if rank['queueType'] == 'RANKED_SOLO_5x5' else 'Ranqueada Flex'
                embed.add_field(
                    name=queue_type,
                    value=f"{rank['tier']} {rank['rank']} - {rank['leaguePoints']} LP\n"
                          f"Vitórias: {rank['wins']} | Derrotas: {rank['losses']}",
                    inline=False
                )
        else:
            embed.add_field(name="Ranque", value="Não ranqueado", inline=False)
            
        await message.edit(content=None, embed=embed)

def setup(bot):
    bot.add_cog(SummonerCog(bot))