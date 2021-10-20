import nextcord as discord
from nextcord import Embed
from nextcord.ext import commands, menus
import sqlite3




import bot.core.modules.backend_commands.message_transformation as message_transformation
import bot.core.modules.user.card_generator as card_generator
import bot.core.modules.user.help_message as help_message
import bot.core.modules.user.parse_stats as parse_stats
import bot.core.modules.user.units_roles as units_roles
import bot.core.modules.utils.log_command as log_command
import bot.core.modules.utils.error_controller as error_controller
from bot.core.configs import roles_config
from bot.core.configs.access_config import settings


client = commands.Bot(command_prefix=settings['botPrefix'], help_command=None)


@client.event
async def on_ready():
    print('[LOG] Bot is ready!')


@client.command()
async def help(ctx):
    # user = ctx.author
    # print(f'[LOG] {user} called command "help"')
    await log_command.command_start(ctx, "help")
    await help_message.send_help_message(ctx)
    await log_command.command_done("help")


@client.command()
async def tank(ctx):
    user = ctx.author
    await log_command.command_start(ctx, "tank")
    guild_id = client.get_guild(settings['guildId'])
    await units_roles.add_role_tank(ctx, user, guild_id)
    print('[LOG] Set role "Tank" command done!')
    await log_command.command_done("tank")


@client.command()
async def plane(ctx):
    user = ctx.author
    await log_command.command_start(ctx, "plane")
    guild_id = client.get_guild(settings['guildId'])
    await units_roles.add_role_plane(ctx, user, guild_id)
    await log_command.command_done("plane")


@client.command()
async def rb(ctx, nickname: discord.Member = None):
    user = ctx.author
    await log_command.command_start(ctx, "rb")
    await parse_stats.get_statistics(ctx, nickname, 'r')
    await log_command.command_done("rb")


@client.command()
async def sb(ctx, nickname: discord.Member = None):
    user = ctx.author
    await log_command.command_start(ctx, "sb")
    await parse_stats.get_statistics(ctx, nickname, 's')
    await log_command.command_done("sb")


@client.command()
async def card(ctx, user: discord.Member = None):
    log_user = ctx.author
    await log_command.command_start(ctx, "card")
    await card_generator.card(ctx, user, client)
    print('[LOG] "card" command done!')


@commands.has_any_role(roles_config.discord_roles['admin'])
@client.command()
async def clear(ctx, amount):
    user = ctx.author
    await log_command.command_start(ctx, "clear")
    await message_transformation.clear_some_messages(ctx, amount)

@client.command()
async def t(ctx):
    await error_controller.user_has_no_roles(ctx)

# @commands.has_any_role(roles_config.discord_roles['admin'])
# @client.command()
# async def rules(ctx):
#     user = ctx.author
#     print(f'[LOG] {user} called command "rules"')
#     await message_transformation.send_rules_to_the_channel(ctx)
#     print('[LOG] "rules" command done!')


# @client.command()
# async def add(ctx, user: discord.Member, stamp_id: int):
#     conn = sqlite3.connect('bot/core/data/user_stamps.db')
#     send_stamp = {}
#     cursor = conn.cursor()
#     cursor.execute(f'''SELECT stamp_id FROM stamps WHERE user_id={user.id}''')
#     stamps = cursor.fetchone()
#     if stamps is not None:
#         stamps = stamps[0]
#
#     print(f'ROW MEDALS: {stamps}')
#     if stamps is None:
#         send_medals[medal_id] = 1
#         c.execute(f'''INSERT INTO medals(user_id, medals) VALUES(\'{user.id}\',\'{send_medals}\')''')
#     else:
#         send_medals = ast.literal_eval(medals)
#         print(f'MEDALS: {send_medals}')
#         if medal_id in send_medals:
#             send_medals[medal_id] += 1
#         else:
#             send_medals[medal_id] = 1
#         c.execute(f'''UPDATE medals SET medals=\'{send_medals}\' WHERE user_id=\'{user.id}\'''')
#     conn.commit()


# class MyEmbedFieldPageSource(menus.ListPageSource):
#     def __init__(self, data):
#         super().__init__(data, per_page=2)
#
#     async def format_page(self, menu, entries):
#         embed = Embed(title="Entries")
#         for entry in entries:
#             embed.add_field(name=entry[0], value=entry[1], inline=True)
#         embed.set_footer(text=f'Page {menu.current_page + 1}/{self.get_max_pages()}')
#         return embed
#
#
#
#
# class MyEmbedDescriptionPageSource(menus.ListPageSource):
#     def __init__(self, data):
#         super().__init__(data, per_page=6)
#
#     async def format_page(self, menu, entries):
#         embed = Embed(title="Entries", description="\n".join(entries))
#         embed.set_footer(text=f'Page {menu.current_page + 1}/{self.get_max_pages()}')
#         return embed
#
#
# @client.command(aliases=["bed"])
# async def rules(ctx):
#     data = [f'Description for entry #{num}' for num in range(1, 51)]
#     pages = menus.ButtonMenuPages(
#         source=MyEmbedDescriptionPageSource(data),
#         clear_buttons_after=True,
#     )
#     await pages.start(ctx)


client.run(settings['botToken'])
