import disnake, env, json
from disnake.ext import commands, tasks
from datetime import datetime
from colorama import init, Style, Fore
from sys import version_info

class utils(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.slash_command(description="Information about how the bot works")
    async def help(self,inter):
        embed = disnake.Embed(
            title="The game of Mute Roulette",
            description="This bot allows you to play the **Mute Roulette** using the Timeout Revolver™️ *(a property of Greenlite Team, we are not liable for any timeouts caused by it)*. <:Basedge:1014852510927818862>\n\nRun the `/roulette` command to try your luck once **every 10 minutes**. By default you play with **1 bullet** (and thus get 1 point for surviving), but you an increase the amount of bullets in the barrel **up to 5** (and thus get 5 points). Your points are **counted up** in the bot's database, and you can use `/leaderboard` to check the **10 members of the server with most points**. If you lose - you get **Timed Out** (muted) for 15 minutes. Server administrators have the ability to **wipe the scores** on their server with `/reset`, if that is required. <:NOTED:885176088920227881>\n\nFor reporting bugs or sending ideas do `/support`, for future updates do `/roadmap`. Good luck and have fun! <:Okayge:993617462388072469>",
            color=0xa352ed
        )
        await inter.send(embed=embed,ephemeral=True)
        print(f'{Fore.LIGHTBLUE_EX}[{datetime.now()}] [COMMND] - {inter.author} used /help{Style.RESET_ALL}')

    @commands.slash_command(description="The support server for bugreports and ideas")
    async def support(self,inter):
        embed = disnake.Embed(
            title="Support Server",
            description="If you want to **report bugs** you found in the bot or **suggest ideas** - hop into the `#support` channel on the server below and drop a message. The server is mostly Russian, but we do support English chatters. <:Okayge:993617462388072469>\n\nhttps://discord.gg/RNSSJatNbq",
            color=0xa352ed
        )
        await inter.send(embed=embed,ephemeral=True)
        print(f'{Fore.LIGHTBLUE_EX}[{datetime.now()}] [COMMND] - {inter.author} used /support{Style.RESET_ALL}')

    @commands.slash_command(description="A look at things that we could implement into the bot in the future")
    async def roadmap(self,inter):
        embed = disnake.Embed(
            title="Roadmap",
            description="Here's a list of things that we plan to implement into this bot in the near future. <:NOTED:885176088920227881>\n*Note that this list is not final, and not all features are actually going to be implemented.*\n\n- Global leaderboards (with an opt-in system, ofc)\n- Variable timeout times (currently hardcoded at 15min)\n- Duels\n- Refactoring cogs (this bot was written in 1 day, and most commands are in a single cog)\nIf you have any more ideas - suggest them through `/support`",
            color=0xa352ed
        )
        await inter.send(embed=embed,ephemeral=True)
        print(f'{Fore.LIGHTBLUE_EX}[{datetime.now()}] [COMMND] - {inter.author} used /roadmap{Style.RESET_ALL}')

    @commands.slash_command(description="Some debug info about the bot")
    async def debug(self,inter):
        embed = disnake.Embed(
            title = "Debug info",
            color = 0xa352ed
        )
        embed.add_field("disnake version", f"`{disnake.__version__}`")
        embed.add_field("python version", f"`{str(version_info[0])+'.'+str(version_info[1])+'.'+str(version_info[2])}`")
        embed.add_field("server time", f"`{str(datetime.now())[:-7]}`")
        await inter.send(embed=embed,ephemeral=True)
        print(f"{Fore.LIGHTCYAN_EX}[{datetime.now()}] [COMMND] - {inter.author} used /debug on {inter.guild.name}{Style.RESET_ALL}")

def setup(bot):
    bot.add_cog(utils(bot))
