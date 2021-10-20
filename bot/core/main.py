import nextcord as discord
from nextcord.ext import commands
import sqlite3

import modules.backend_commands.message_transformation as message_transformation
import modules.user.card_generator as card_generator
import modules.user.help_message as help_message
import modules.user.parse_stats as parse_stats
import modules.user.units_roles as units_roles
from configs import roles_config
from configs.access_config import settings

client = commands.Bot(command_prefix=settings['botPrefix'], help_command=None)


@client.event
async def on_ready():
    print('[LOG] Bot is ready!')


@client.command()
async def help(ctx):
    user = ctx.author
    print(f'[LOG] {user} called command "help"')
    await help_message.send_help_message(ctx)
    print('[LOG] Help command done!')


@client.command()
async def tank(ctx):
    user = ctx.author
    print(f'[LOG] {user} called command "tank"')
    guild_id = client.get_guild(settings['guildId'])
    await units_roles.add_role_tank(ctx, user, guild_id)
    print('[LOG] Set role "Tank" command done!')


@client.command()
async def plane(ctx):
    user = ctx.author
    print(f'[LOG] {user} called command "plane"')
    guild_id = client.get_guild(settings['guildId'])
    await units_roles.add_role_plane(ctx, user, guild_id)
    print('[LOG] Set role "Plane" command done!')


@client.command()
async def rb(ctx, nickname: discord.Member = None):
    user = ctx.author
    print(f'[LOG] {user} called command "rb"')
    await parse_stats.get_statistics(ctx, nickname, 'r')
    print('[LOG] "rb" command done!')


@client.command()
async def sb(ctx, nickname: discord.Member = None):
    user = ctx.author
    print(f'[LOG] {user} called command "sb"')
    await parse_stats.get_statistics(ctx, nickname, 's')
    print('[LOG] "sb" command done!')


@client.command()
async def card(ctx, user: discord.Member = None):
    log_user = ctx.author
    print(f'[LOG] {log_user} called command "card"')
    await card_generator.card(ctx, user, client)
    print('[LOG] "card" command done!')


@commands.has_any_role(roles_config.discord_roles['admin'])
@client.command()
async def clear(ctx, amount):
    user = ctx.author
    print(f'[LOG] {user} called command "clear"')
    await message_transformation.clear_some_messages(ctx, amount)


@commands.has_any_role(roles_config.discord_roles['admin'])
@client.command()
async def rules(ctx):
    user = ctx.author
    print(f'[LOG] {user} called command "rules"')
    await message_transformation.send_rules_to_the_channel(ctx)
    print('[LOG] "rules" command done!')


@client.command()
async def stamp(ctx):
    conn = sqlite3.connect('orders.db')


client.run(settings['botToken'])
