import discord
from discord.ext import commands
from discord.utils import get
from access_config import settings as settings

client = commands.Bot(command_prefix=settings['prefix'])


@client.event
async def on_ready():

    print('[LOG] Bot is ready!')


@client.command()
async def hello(ctx):  # Создаём функцию и передаём аргумент ctx.
    # Объявляем переменную author и записываем туда информацию об авторе.
    author = ctx.message.author

    await ctx.send(f'Hello, {author.mention}!')


client.run(settings['token'])
