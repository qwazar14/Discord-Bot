import asyncio
import os

import nextcord
import nextcord as discord
from nextcord.ext import commands

import modules.utils.error_controller as error_controller
import modules.utils.message_transformation as message_transformation
import modules.utils.ranks as rank_system
from configs import roles_config
from configs.access_config import settings
from modules.user import member_roles
from configs import roles_config, util_config
from configs.access_config import settings
from modules.user import member_roles
# from modules.utils.registration_menu.registration_functions import timeout_error, get_user_response, \
#     replace_comma_to_do, SquadronMenu, user_without_squadron
import modules.utils.registration_menu.registration_functions as registration_functions


intents = discord.Intents.all()
client = commands.Bot(command_prefix=settings['botPrefix'], intents=intents)


@client.event
async def on_ready():
    print('[INFO] Bot is ready!')


@client.event
async def on_member_join(member):
    guild_id = client.get_guild(settings['guildId'])
    await member_roles.new_player_joined(member, guild_id)
    print(f"[INFO] {member} was given the main roles.")


@client.event
async def on_command(ctx):
    print(f'[INFO] {ctx.author} called command {ctx.command}:\nArgs: {ctx.args}\nKwargs: {ctx.kwargs}')


'''@client.command()
async def help(ctx):
    # user = ctx.author
    await help_message.send_help_message(ctx)
'''

'''
@client.command()
async def rules(ctx):
    await message_transformation.send_rules_to_the_channel(ctx)
'''

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

@commands.has_any_role(roles_config.discord_roles['admin'])
@client.command()
async def mmenu(ctx, k: int):
    embed=discord.Embed(title='⠀'*14+'Музыкальное меню 16', color=0xe100ff)
    value = '═'*int(k-1)+'🞈'+'─'*int(49-k)+'\n'+'⠀'*17+'##:##:##/##:##:##'
    embed.add_field(name='\u200b', value=f'{value}')
    await ctx.send(embed=embed)


@commands.has_any_role(roles_config.discord_roles['admin'])
@client.command()
async def rules(ctx):
    embed=discord.Embed(title='Общие правила', color=0xe100ff)
    embed.add_field(name="\u200b", value='```css\n1.1 На этом сервере не допускается расовая нетерпимость или крайняя ненависть любого рода.\n[Бан или предупреждение, в зависимости от содержания]```', inline=False)
    
    embed.add_field(name="\u200b", value='```css\n1.2 Не будьте токсиком, который портит веселье другим. Это включает в себя нацеливание на одного человека и обсирание его.\n[Бан или предупреждение, в зависимости от содержания]```', inline=False)
    
    embed.add_field(name="\u200b", value='```css\n1.3 Не сливайте личную информацию о других членах сервера без их разрешения. Это относится и к личке.\n[Предупреждение или бан в зависимости от серьезности утечки]```', inline=False)
    
    embed.add_field(name="\u200b", value='```css\n1.4 Не публикуйте nsfw-контент вне #nsfw.\n[Бан]```', inline=False)
    
    embed.add_field(name="\u200b", value='```css\n1.5 Не выдавайте себя за ботов или любого члена сервера. (Через имя, ник или картинку профиля)\n[Предупреждение и бан в случае продолжения]```', inline=False)
    
    embed.add_field(name="\u200b", value='```css\n1.6 Запрещен спам ЛЮБОГО рода, включая @everyone/@here спам, спам реакции, копирование/вставка текста, @mentions в AFK.\n[Предупреждению и бан в случае продолжения.]```', inline=False)
    
    embed.add_field(name="\u200b", value='```css\n1.7 Не пингуйте роли без веской причины. Пингуйте роли только в экстренных случаях.\n[Предупреждение]```', inline=False)
    
    embed.add_field(name="\u200b", value='```css\n1.8 Не выпрашивать роль/звание. Нам это не нужно, и если мы посчитаем, что вы заслуживаете роли, мы вам ее дадим.\n[Предупреждение]```', inline=False)
    
    embed.add_field(name="\u200b", value='```css\n1.9 Используйте каналы по назначению, (в каналах «музыка» – запускайте музыку и т.д)\n[Устное предупреждение и предупреждение в случае продолжения]```', inline=False)
    
    embed.add_field(name="\u200b", value='```css\n1.10 Не вступайте в дискуссию с офицерами на сервере после решения о наказании (например, получения предупреждения), если вы считаете, что предупреждение было неправильным, пожалуйста, решите этот вопрос в личке с тем, кто выписал предупредил.\n[Предупреждение]```', inline=False)
    
    await ctx.send(embed=embed)


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
