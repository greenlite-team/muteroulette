import disnake, env, json, random, itertools
from disnake.ext import commands, tasks
from datetime import datetime
from colorama import init, Style, Fore

class roulette(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.autosave.start()

    def cog_unload(self):
        self.savedb()
        self.autosave.cancel()

    @commands.cooldown(rate=1,per=600.0,type=commands.BucketType.member)
    @commands.slash_command(description="Try your luck and shoot the Timeout Revolver™️!")
    async def roulette(self,inter,bullets:int=commands.Param(description="Amount of bullets in barrel; default=1",default=1,ge=1,le=5)):
        result = random.randint(1, 6) # TODO: make an actual pure RNG, not pseudorandom
        if result <= bullets: # loss
            if inter.author.guild_permissions.administrator:
                await inter.send("The Timeout Revolver™️ would fire here, but you're an Administrator and cannot be timed out. <:Shruge:1015541861022171167>")
                print(f'{Fore.LIGHTBLUE_EX}[{datetime.now()}] [COMMND] - {inter.author} shot the revolver with {bullets} bullets and died (but is an admin){Style.RESET_ALL}')
            else:
                await inter.send("*Pow!* The Timeout Revolver™️ shoots, and you get timed out for `15` minutes! <:Deadge:1015534892660031528>")
                await inter.author.timeout(duration=900,reason="Lost the Timeout Roulette")
                print(f'{Fore.LIGHTBLUE_EX}[{datetime.now()}] [COMMND] - {inter.author} shot the revolver with {bullets} bullets and died{Style.RESET_ALL}')
        else: # win
            newbullets = self.add(user=inter.author, points=bullets)
            await inter.send(f"*Click!* The Timeout Revolver™️ does not fire, and you survive the shot! <:WICKED:1014451909416976394>\n`+{bullets}` point(s) to your score, now at `{newbullets} points`")
            print(f'{Fore.LIGHTBLUE_EX}[{datetime.now()}] [COMMND] - {inter.author} shot the revolver with {bullets} bullets and survived{Style.RESET_ALL}')    

    @roulette.error
    async def roulette_error(self,inter,error):
        if isinstance(error,commands.CommandOnCooldown):
            await inter.send("You can only play the roulette once every `10 minutes`.",ephemeral=True)
    
    # Honestly, I hate using these functions.
    # Yes, they are simple, they do their thing.
    # But they were originally written about 1 year ago (as of 2022-09-03)
    # So I really want to find new ways to interact with this stuff.
    # Mostly because they interact with the DB in-memory, and then they have to save it.
    # Which means, that shutting down the bot with Ctrl+C usually tends to not save the DB, or revert it to last state.
    # Which IS going to be problematic, when you're working with stuff like leaderboards.

    @tasks.loop(seconds=600.0)
    async def autosave(self):
        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(self.bot.db, file, indent=4)

    def savedb(self):
        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(self.bot.db, file, indent=4)
            print(f"{Fore.LIGHTBLUE_EX}[{datetime.now()}] [I] [DATABS] - Saved.{Style.RESET_ALL}")

    def loaddb(self):
        with open("data.json", "r", encoding="utf-8") as file:
            self.bot.db = json.load(file)
            print(f"{Fore.LIGHTBLUE_EX}[{datetime.now()}] [I] [DATABS] - Loaded.{Style.RESET_ALL}")

    def getuser(self,user: disnake.Member):
        gid = str(user.guild.id)
        uid = str(user.id)
        if not gid in self.bot.db: self.bot.db[gid] = {}
        if not uid in self.bot.db[gid]: self.bot.db[gid][uid] = 0
        return self.bot.db[gid][uid]

    def add(self,user: disnake.Member,points: int):
        gid = str(user.guild.id)
        uid = str(user.id)
        points += self.getuser(user) 
        self.bot.db[gid][uid] = points
        return self.bot.db[gid][uid]

    def reset(self,guild: disnake.Guild):
        gid = str(guild.id)
        self.bot.db[gid] = {}

    @commands.is_owner()
    @commands.slash_command(description="DEV: dump database to file",guild_ids=[883778577609412660])
    async def dump(self,inter):
        self.savedb()
        await inter.send(f"`{self.bot.db}`\nDumped database to `data.json`",ephemeral=True)

    @commands.is_owner()
    @commands.slash_command(description="DEV: load database from file",guild_ids=[883778577609412660])
    async def load(self,inter):
        self.loaddb()
        await inter.send(f"`{self.bot.db}`\nLoaded database from `data.json`",ephemeral=True)

    @commands.has_permissions(administrator=True)
    @commands.slash_command(description="Wipe server scores")
    async def reset(self,inter):
        self.reset(inter.guild)
        await inter.send("Server scores successfully wiped!")
        print(f'{Fore.LIGHTBLUE_EX}[{datetime.now()}] [COMMND] - {inter.author} wiped scores for {inter.guild}{Style.RESET_ALL}')

    @commands.slash_command(description="Show leaderboard for server")
    async def leaderboard(self,inter):
        try:
            lb = self.bot.db[str(inter.guild.id)]
            sortedlb = dict(sorted(lb.items(), key=lambda item:item[1],reverse=True))
            cutlb = dict(itertools.islice(sortedlb.items(), 10))
            desc = ""
            keys = list(cutlb.keys())
            for key in keys:
                desc += f"`{keys.index(key)+1}.` <@{int(key)}>: {cutlb[key]} points\n"
            embed = disnake.Embed(
                title="Top members by points <:NOTED:885176088920227881>",
                description=desc,
                color=0xa352ed
            )
            embed.set_author(name=inter.guild,icon_url=inter.guild.icon.url)
            await inter.send(embed=embed)
            print(f'{Fore.LIGHTBLUE_EX}[{datetime.now()}] [COMMND] - {inter.author} checked leaderboard for {inter.guild}{Style.RESET_ALL}')
        except KeyError:
            await inter.send("Cannot find guild in database, try running `/roulette` until somebody gets a point.\nThe leaderboard should become available after that.\nThis could also be caused by a bug in code, but unlikely. <:Shruge:1015541861022171167>")

def setup(bot):
    bot.add_cog(roulette(bot))