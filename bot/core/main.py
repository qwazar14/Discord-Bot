import os

import nextcord
import nextcord as discord
from nextcord.ext import commands

import bot.core.modules.utils.error_controller as error_controller

from bot.core.configs import roles_config
from bot.core.configs.access_config import settings
from bot.core.modules.user import member_roles


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


# @client.command()
# async def rules(ctx):
#     embed=discord.Embed(title="1. Общие правила", color=0xe100ff)
#     embed.set_thumbnail(url="https://i.imgur.com/mhSJtPm.png")
#     embed.add_field(name="1.1 На этом сервере не допускается расовая нетерпимость или крайняя ненависть любого рода.", value="Наказание: Бан или предупреждение, в зависимости от содержания", inline=True)
#     embed.add_field(name="1.2 Не будьте токсиком, который портит веселье другим. Это включает в себя нацеливание на одного человека и обсирание его.", value="Наказание: Бан или предупреждение, в зависимости от содержания", inline=True)
#     embed.add_field(name="1.3 Не сливайте личную информацию о других членах сервера без их разрешения. Это относится и к личке.", value="Наказание: предупреждение или бан в зависимости от серьезности утечки", inline=True)
#     embed.add_field(name="1.4 Не публикуйте nsfw-контент вне #nsfw.", value="Наказание: Бан", inline=True)
#     embed.add_field(name="1.5 Не выдавайте себя за ботов или любого члена сервера. (Через имя, ник или картинку профиля)", value="Наказание: Предупреждение и бан в случае продолжения", inline=True)
#     embed.add_field(name="1.6 Запрещен спам ЛЮБОГО рода, включая @everyone/@here спам, спам реакции, копирование/вставка текста, @mentions в AFK.", value="Наказание: Это приведет к предупреждению и бану в случае продолжения.", inline=True)
#     embed.add_field(name="1.7 Не пингуйте роли без веской причины. Пингуйте роли только в экстренных случаях.", value="Наказание: Предупреждение", inline=True)
#     embed.add_field(name="1.8 Не выпрашивать роль/звание. Нам это не нужно, и если мы посчитаем, что вы заслуживаете роли, мы вам ее дадим.", value="Наказание: Предупреждение", inline=True)
#     embed.add_field(name="1.9 Используйте каналы по назначению, (в каналах «музыка» – запускайте музыку и т.д)", value="Наказание: Устное предупреждение и предупреждение в случае продолжения", inline=True)
#     embed.add_field(name="1.10 Не вступайте в дискуссию с офицерами на сервере после решения о наказании (например, получения предупреждения), если вы считаете, что предупреждение было неправильным, пожалуйста, решите этот вопрос в личке с тем, кто выписал предупредил.", value="Наказание: Предупреждение", inline=True)
#     await ctx.send(embed=embed)


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
