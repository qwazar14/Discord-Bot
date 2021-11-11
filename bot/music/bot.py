import nextcord as discord
import pymysql
import sys, os

from nextcord.ext import commands, tasks
from cogs import music


from configs.bd_config import CONFIG

id = int(sys.argv[1])
token = sys.argv[2]

con = pymysql.connect(
            host=CONFIG['host'],
            user=CONFIG['user'],
            password=CONFIG['password'],
            database=CONFIG['db']) 
cursor = con.cursor()

intents = discord.Intents.all()
client = commands.Bot(command_prefix=f'm{id}!', intents=intents)

@client.event
async def on_ready():
    music.setup(client, id)
    print(f'BOT-{id} IS READY')

client.run(token)

