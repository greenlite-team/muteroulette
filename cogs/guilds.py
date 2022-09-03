import disnake
from disnake.ext import commands
from colorama import Style, Fore
from datetime import datetime

class guilds(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_guild_remove(self,guild):
        logchannel = await self.bot.fetch_channel(886449232486227998)
        embed = disnake.Embed(
            title=f"Вышел с сервера {guild}",
            description=f"Кол-во участников: **{guild.member_count}**",
            colour=0xff0000
        )
        await logchannel.send(embed=embed)
        print(f'{Fore.LIGHTRED_EX}[{datetime.now()}] [-GUILD] - Bot left guild {guild}{Style.RESET_ALL}')

    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        logchannel = await self.bot.fetch_channel(886449232486227998)
        embed = disnake.Embed(
            title=f"Зашел на сервер {guild}",
            description=f"Кол-во участников: **{guild.member_count}**",
            colour=0x00ff00
        )
        await logchannel.send(embed=embed)
        print(f'{Fore.LIGHTGREEN_EX}[{datetime.now()}] [+GUILD] - Bot joined guild {guild}{Style.RESET_ALL}')
        
def setup(bot):
    bot.add_cog(guilds(bot))