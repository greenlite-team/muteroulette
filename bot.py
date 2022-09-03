import disnake, env, json, time
from disnake.ext import commands
from datetime import datetime
from colorama import init, Style, Fore
from os import listdir

init()
intents = disnake.Intents.default()
if env.TEST:
    bot = commands.InteractionBot(test_guilds=[883778577609412660], intents=intents)
else:
    bot = commands.InteractionBot(intents=intents)

with open("data.json", "r", encoding="utf-8") as file:
    db = json.load(file)
    bot.db = db

for cog in listdir('./cogs'):
    if cog.endswith('.py'):
        bot.load_extension(f'cogs.{cog[:-3]}')
        print(f'{Fore.GREEN}[{datetime.now()}] [LAUNCH] - Loaded cog {cog}{Style.RESET_ALL}')

@bot.event
async def on_ready():
    print(f'{Fore.LIGHTGREEN_EX}[{datetime.now()}] [LAUNCH] - Launched as "{bot.user}"{Style.RESET_ALL}')

@bot.slash_command(description="Check the bot's ping")
async def ping(inter):
    await inter.send(f"Pong! The ping is `{round(bot.latency*1000)}` ms",ephemeral=True)

@commands.is_owner()
@bot.slash_command(description="DEV: Reload cogs", guild_ids=[883778577609412660])
async def reload(inter):
    for cog in listdir('./cogs'):
                if cog.endswith('.py'):
                    bot.reload_extension(f'cogs.{cog[:-3]}')
                    print(f'{Fore.GREEN}[{datetime.now()}] [LAUNCH] - Reloaded cog "{cog}"{Style.RESET_ALL}') 
    await inter.send('All cogs reloaded!', ephemeral=True)

bot.run(env.TOKEN)
