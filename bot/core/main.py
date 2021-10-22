import datetime
from typing import Union

import nextcord as discord
from nextcord import role
from nextcord import components
import nextcord
from nextcord.components import ActionRow, Button
from nextcord.ext import commands
from nextcord.ext.commands import errors
from nextcord.types.components import ButtonComponent, ButtonStyle
from nextcord.ui import Button
import modules.user.card_generator as card_generator
import modules.user.help_message as help_message
import modules.user.parse_stats as parse_stats
import modules.user.units_roles as units_roles
import modules.utils.error_controller as error_controller
import modules.utils.log_command as log_command
import modules.utils.message_transformation as message_transformation
from configs import roles_config
from configs.access_config import settings

client = commands.Bot(command_prefix=settings['botPrefix'], help_command=None)

@client.command()
async def up(ctx):

    class RankSys(nextcord.ui.View):

        @discord.ui.button(label = 'Повысить', style = nextcord.ButtonStyle.green)
        async def rank_up(self, button, interaction):
            button.disabled = True
            self.up = True
            self.stop()

        @discord.ui.button(label = 'Отказ', style = nextcord.ButtonStyle.red)
        async def deny(self, button, interaction):
            button.disabled = True
            self.up = False
            self.stop()

    view = RankSys()
    all_roles_dict = roles_config.officer_roles | roles_config.soldier_roles
    member_roles_set = set([role.id for role in ctx.author.roles])
    rank_roles = list(all_roles_dict.keys())
    role_id = list(member_roles_set.intersection(rank_roles))[0]
    now = datetime.datetime.now(datetime.timezone.utc)

    if all_roles_dict[role_id] in ['OF-8','OF-9','OF-10']:
            await ctx.('Вы заняли максимальное звание в нашем полке. Подача заявки на повышение для вас закрыта.')
            return

    timedelta = now - ctx.author.joined_at
    seconds = timedelta.total_seconds()
    days = seconds // 86400
    month = days // 30
    days = days - (month * 30)

    datestr = f'{int(month)} месяцев и {int(days)} дней'

    buttons = [Button(style=discord.ButtonStyle.success, label='Повысить'),Button(style=discord.ButtonStyle.danger, label='Отказ')]

    embed=discord.Embed(title="Повышение", color=0xf2930d)
    embed.add_field(name=f"Игрок {ctx.author.nick} запрашивает повышение.", value=f"Текущее звание: {all_roles_dict[role_id]}", inline=True)
    embed.set_footer(text=f"На сервере {datestr}")
    await ctx.send(embed=embed, view=view)
    await view.wait()
    if view.up:
        new_role_id = rank_roles[rank_roles.index(role_id)+1]
        await ctx.author.remove_roles(ctx.guild.get_role(role_id))
        await ctx.author.add_roles(ctx.guild.get_role(new_role_id))
        await ctx.author.send('Ваc повысили.')
    else:
        await ctx.author.send('Вам отказали в повышение. Следующий запрос возможен через неделю.')


    
@client.event
async def on_ready():
    print('[LOG] Bot is ready!')

@client.event
async def on_command(ctx):
    print(f'[LOG] {ctx.author} called command {ctx.command}:\nArgs: {ctx.args}\nKwargs: {ctx.kwargs}')

'''@client.command()
async def help(ctx):
    # user = ctx.author
    await help_message.send_help_message(ctx)
'''

@client.command()
async def rules(ctx):
    await message_transformation.send_rules_to_the_channel(ctx)

@client.command()
async def t(ctx):
    await error_controller.user_has_no_roles(ctx)

@commands.has_any_role(roles_config.discord_roles['admin'])
@client.command()
async def reload(ctx, extension):
    result = ""
    if extension == "all":
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py") and filename != "db.py":
                try:
                    client.unload_extension(f"cogs.{filename[:-3]}")
                    client.load_extension(f"cogs.{filename[:-3]}")
                except Exception as e:
                    result += f"[ERROR] reload **{filename}:** {e}\n"
                else:
                    result += f"**{filename[:-3]}** reloaded!\n"
    else:
        try:
            client.unload_extension(f"cogs.{extension}")
            client.load_extension(f"cogs.{extension}")
        except Exception as e:
            result += f"Error reload **{extension}:** {e}\n\n"
        else:
            await ctx.send(f"**{extension}** reloaded!")
    if result != "":
        await ctx.send(result)

@commands.has_any_role(roles_config.discord_roles['admin'])
@client.command()
async def unload(ctx, extension):
    result = ""
    if extension == "all":
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py") and filename != "db.py":
                try:
                    client.unload_extension(f"cogs.{filename[:-3]}")
                except Exception as e:
                    result += f"[ERROR] unload **{filename}:** {e}\n"
                else:
                    result += f"**{filename[:-3]}** unloaded!\n"
    else:
        try:
            client.unload_extension(f"cogs.{extension}")
        except Exception as e:
            result += f"[ERROR] unload **{extension}:** {e}\n\n"
        else:
            await ctx.send(f"**{extension}** unloaded!")
    if result != "":
        await ctx.send(result)

@commands.has_any_role(roles_config.discord_roles['admin'])
@client.command()
async def load(ctx, extension):
    result = ""
    if extension == "all":
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py") and filename != "db.py":
                try:
                    client.load_extension(f"cogs.{filename[:-3]}")
                except Exception as e:
                    result += f"[ERROR] load **{filename}:** {e}\n\n"
                else:
                    await ctx.send(f"**{filename[:-3]}** loaded!")
    else:
        try:
            client.load_extension(f"cogs.{extension}")
        except Exception as e:
            result += f"[ERROR] load **{extension}:** {e}\n\n"
        else:
            await ctx.send(f"**{extension}** loaded!")
    if result != "":
        await ctx.send(result)
        
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

# settings['botToken']
client.run('OTAwODU5NjMwMzI0OTczNjA4.YXHc6Q.o1lUq8KaaFsl3ml4tSxEOPu0UFs')
