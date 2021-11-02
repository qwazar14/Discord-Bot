import asyncio
import datetime
import os
import re

import nextcord
import nextcord as discord

from nextcord.components import Button
from nextcord.ext import commands

import modules.utils.error_controller as error_controller
import modules.utils.message_transformation as message_transformation
from configs import roles_config
from configs.access_config import settings

import modules.utils.ranks as rank_system
from configs import roles_config
from configs.access_config import settings
from modules.user import member_roles

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


@client.command(pass_context=True)
async def registration_menu(ctx):
    class RegistrationMenu(nextcord.ui.View):

        @discord.ui.button(label='Подать заявку в полк', style=nextcord.ButtonStyle.green)
        async def join_squadron(self, button, interaction):
            user = interaction.user
            # a = await interaction.response.send_message(content='*Введите ник в игре* ', ephemeral=True)
            # await message_transformation.clear_last_user_message(ctx)
            # print(a)
            await interaction.response.send_message(content='*Введите ник в игре* ', ephemeral=True)
            try:

                msg_id = await client.wait_for("message", timeout=5, check=lambda
                    m: m.author == interaction.user and m.channel == interaction.channel)
                nickname_user = msg_id.content

            except asyncio.TimeoutError:
                await ctx.send("Извините, вы не ответили вовремя! Повторите попытку")

            await interaction.followup.send(content='*Как Вас зовут?*', ephemeral=True)
            try:
                msg_id = await client.wait_for("message", timeout=5, check=lambda
                    m: m.author == interaction.user and m.channel == interaction.channel)  # 30 seconds to reply

                name_user = msg_id.content

            except asyncio.TimeoutError:
                await ctx.send("Извините, вы не ответили вовремя! Повторите попытку")

            await interaction.followup.send(content='*Введите ваш максимальный БР*', ephemeral=True)
            try:
                msg_id = await client.wait_for("message", timeout=5, check=lambda
                        m: m.author == interaction.user and m.channel == interaction.channel)

                br_user = max([float(i) for i in msg_id.content.replace(',', '.').split()])
                new_nickname = (f"[{br_user}] {nickname_user} ({name_user})")
                await user.edit(nick=new_nickname)


            except asyncio.TimeoutError:
                await ctx.send("Извините, вы не ответили вовремя! Повторите попытку")






        @discord.ui.button(label='Друг полка', style=nextcord.ButtonStyle.blurple)
        async def squadron_friend(self, button, interaction):

            a = await interaction.response.send_message(content='*Введите ник в игре* ', ephemeral=True)
            # await message_transformation.clear_last_user_message(ctx)
            print(a)
            try:

                msg_id = await client.wait_for("message", timeout=30, check=lambda
                    m: m.author == interaction.user and m.channel == interaction.channel)
                nickname_user = msg_id.content

            except asyncio.TimeoutError:
                await ctx.send("Sorry, you didn't reply in time!")

            await interaction.followup.send(content='*Как Вас зовут?*', ephemeral=True)
            try:
                msg_id = await client.wait_for("message", timeout=30, check=lambda
                    m: m.author == interaction.user and m.channel == interaction.channel)  # 30 seconds to reply

                name_user = msg_id.content

            except asyncio.TimeoutError:
                await ctx.send("Извините, вы не ответили вовремя! Повторите попытку")

            class SquadronMenu(nextcord.ui.View):

                @discord.ui.button(label='Да', style=nextcord.ButtonStyle.green)
                async def squadron_friend1(self, button, interaction):
                    await interaction.response.send_message(content='*Введите клантег полка(например*', ephemeral=True)

                @discord.ui.button(label='Нет', style=nextcord.ButtonStyle.red)
                async def squadron_friend2(self, button, interaction):
                    await interaction.response.send_message(content='*Регистрация завершена*', ephemeral=True)

            view_squadron_buttons = SquadronMenu()
            await interaction.followup.send(content='*Вы состоите в полку?*', ephemeral=True,
                                            view=view_squadron_buttons)
            try:
                msg_id = await client.wait_for("message", timeout=30, check=lambda
                    m: m.author == interaction.user and m.channel == interaction.channel)
                await ctx.send(f"{nickname_user} ({name_user})")


            except asyncio.TimeoutError:
                await ctx.send("Извините, вы не ответили вовремя! Повторите попытку")


    view = RegistrationMenu()
    rank = rank_system.get_member_rank(ctx.author, str=True)

    embed = discord.Embed(title="Вы попали на сервер полка GG Company",
                          description="**Если вы хотите вступить в полк, нажмите кнопку 'Подать заявку'**",
                          color=0xe100ff)
    embed.set_thumbnail(url="https://i.imgur.com/mhSJtPm.png")
    embed.add_field(name="Если вы зашли поиграть с друзьями, нажмите кнопку 'Друг полка'",
                    value="Нажимая кнопку вы автоматически соглашаетесь с правилами в канале <#877276991412379709>",
                    inline=False)

    message = await ctx.send(embed=embed, view=view)




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
