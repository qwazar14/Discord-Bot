import discord
from discord.ext import commands

import roles_config
from access_config import settings as settings

client = commands.Bot(command_prefix=settings['botPrefix'], help_command=None)


@client.event
async def on_ready():
    print('[LOG] Bot is ready!')


@client.command()
async def help(ctx):
    print('[LOG] called command "help"')
    await ctx.send("Custom help command")
    print('[LOG] Help command done!')


@client.command()
async def tank(ctx, user: discord.Member):
    print(f'[LOG] {user} called command "tank"')
    guild = client.get_guild(settings['guildId'])
    await user.add_roles(guild.get_role(roles_config.unit_roles['tanks']))
    await ctx.message.add_reaction('✅')
    await ctx.message.delete(delay=5)
    print('[LOG] Set role "Tank" command done!')


@client.command()
async def plane(ctx, user: discord.Member):
    print(f'[LOG] {user} called command "plane"')
    guild = client.get_guild(settings['guildId'])
    await user.add_roles(guild.get_role(roles_config.unit_roles['planes']))
    await ctx.message.add_reaction('✅')
    await ctx.message.delete(delay=5)
    print('[LOG] Set role "Plane" command done!')


@client.command()
async def ship(ctx, user: discord.Member):
    print(f'[LOG] {user} called command "ship"')
    guild = client.get_guild(settings['guildId'])
    await user.add_roles(guild.get_role(roles_config.unit_roles['ship']))
    await ctx.message.add_reaction('✅')
    await ctx.message.delete(delay=5)
    print('[LOG] Set role "Ship" command done!')

@client.command()
async def rules():
    pass



client.run(settings['botToken'])
