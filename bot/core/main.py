import asyncio
import os

import nextcord
import nextcord as discord
from nextcord.ext import commands

import modules.utils.error_controller as error_controller
import modules.utils.message_transformation as message_transformation
import modules.utils.ranks as rank_system
from bot.core.configs import roles_config, util_config
from bot.core.configs.access_config import settings
from bot.core.modules.user import member_roles
# from bot.core.modules.utils.registration_menu.registration_functions import timeout_error, get_user_response, \
#     replace_comma_to_do, SquadronMenu, user_without_squadron
import bot.core.modules.utils.registration_menu.registration_functions as registration_functions

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
        guild_id = client.get_guild(settings['guildId'])

        @discord.ui.button(label='Подать заявку в полк', style=nextcord.ButtonStyle.green)
        async def join_squadron(self, button, interaction, timeout_error_call=True, guild_id=guild_id):
            user = interaction.user

            await interaction.response.send_message(content='Введите ник в игре *(у вас есть 30 секунд)* ',
                                                    ephemeral=True)
            try:
                nickname_user = await registration_functions.get_user_response(client, interaction)
                await interaction.edit_original_message(content='Как Вас зовут? *(у вас есть 30 секунд)*')

            except asyncio.TimeoutError:
                timeout_error_call = await registration_functions.timeout_error(interaction)

            if timeout_error_call is not False:

                try:
                    name_user = await registration_functions.get_user_response(client, interaction)

                    await interaction.edit_original_message(
                        content='Введите ваш максимальный БР *(у вас есть 30 секунд)*')
                except asyncio.TimeoutError:
                    timeout_error_call = await registration_functions.timeout_error(interaction)

            # class UnitMenu(nextcord.ui.View):
            #
            #     @discord.ui.button(label='Танкист', style=nextcord.ButtonStyle.green)
            #     async def check_user_tank(self, interaction):
            #         try:
            #             await user.add_roles(guild_id.get_role(roles_config.unit_roles['tanks']))
            #         except asyncio.TimeoutError:
            #             await registration_functions.timeout_error(interaction)
            #
            #     @discord.ui.button(label='Пилот', style=nextcord.ButtonStyle.blurple)
            #     async def check_user_plane(self, interaction):
            #         try:
            #             await user.add_roles(guild_id.get_role(roles_config.unit_roles['planes']))
            #         except asyncio.TimeoutError:
            #             await registration_functions.timeout_error(interaction)
            #
            #     @discord.ui.button(label='Универсал', style=nextcord.ButtonStyle.red)
            #     async def check_user_universal(self, interaction):
            #         try:
            #             await user.add_roles(guild_id.get_role(roles_config.unit_roles['tanks']))
            #             await user.add_roles(guild_id.get_role(roles_config.unit_roles['planes']))
            #         except asyncio.TimeoutError:
            #             await registration_functions.timeout_error(interaction)

            # if timeout_error_call is not False:
            #     try:
            #         view_squadron_buttons = UnitMenu()
            #     except asyncio.TimeoutError:
            #         await registration_functions.timeout_error(interaction)
            #     await interaction.followup.send(content='*Выберите ваш род войск*', ephemeral=True,
            #                                     view=view_squadron_buttons)

            if timeout_error_call is not False:

                # await interaction.followup.send(content='*Введите ваш максимальный БР*', ephemeral=True)
                try:
                    br_msg_content = await registration_functions.get_user_response(client, interaction)
                    await interaction.edit_original_message(content='*Регистрация завершена*')
                    br_user = await registration_functions.replace_comma_to_do(br_msg_content)
                    new_nickname = f"[{br_user}] {nickname_user} ({name_user})"
                    await user.edit(nick=new_nickname)
                    await user.add_roles(guild_id.get_role(roles_config.util_categories['rank_category']))
                    await user.add_roles(guild_id.get_role(roles_config.util_categories['unit_type_category']))
                    await user.add_roles(guild_id.get_role(roles_config.util_categories['optional_category']))
                    await user.add_roles(guild_id.get_role(roles_config.util_categories['general_category']))
                    await user.add_roles(guild_id.get_role(roles_config.general_category_roles['player']))
                    await user.remove_roles(guild_id.get_role(roles_config.general_category_roles['new_player']))
                    await user.add_roles(guild_id.get_role(rank_system.get_rank_id_by_name('OR-1')))
                    # await registration_functions.end_registration(self, interaction)

                except asyncio.TimeoutError:
                    await registration_functions.timeout_error(interaction)

        @discord.ui.button(label='Друг полка', style=nextcord.ButtonStyle.blurple)
        async def squadron_friend(self, button, interaction, timeout_error_call=True):

            user = interaction.user

            await interaction.response.send_message(content='Введите ник в игре *(у вас есть 30 секунд)* ',
                                                    ephemeral=True)
            try:
                nickname_user = await registration_functions.get_user_response(client, interaction)
                await interaction.edit_original_message(content='Как Вас зовут? *(у вас есть 30 секунд)*')

            except asyncio.TimeoutError:
                timeout_error_call = await registration_functions.timeout_error(interaction)

            if timeout_error_call is not False:
                # await interaction.followup.send(content='*Как Вас зовут?*', ephemeral=True)
                try:
                    name_user = await registration_functions.get_user_response(client, interaction)
                    # await interaction.edit_original_message(content='Как Вас зовут? *(у вас есть 30 секунд)*')

                except asyncio.TimeoutError:
                    timeout_error_call = await registration_functions.timeout_error(interaction)

                # if timeout_error_call is not False:

                class SquadronMenu(nextcord.ui.View):

                    @discord.ui.button(label='Да', style=nextcord.ButtonStyle.green)
                    async def get_user_squadron(self, interaction):
                        await interaction.response.send_message(content='*Введите клантег полка(например*',
                                                                ephemeral=True)
                        try:
                            squadron_user = await registration_functions.get_user_response(client, interaction)
                            new_nickname = f"[{squadron_user}] {nickname_user} ({name_user})"
                            await ctx.send()
                            await user.edit(nick=new_nickname)
                        except asyncio.TimeoutError:
                            await registration_functions.timeout_error(interaction)

                    @discord.ui.button(label='Нет', style=nextcord.ButtonStyle.red)
                    async def end_user_registration(self, interaction):
                        new_nickname = f"[-] {nickname_user} ({name_user})"
                        await ctx.send(new_nickname)
                        await user.edit(nick=new_nickname)
                        await registration_functions.end_registration(self, interaction)

                if timeout_error_call is not False:
                    view_squadron_buttons = SquadronMenu()
                    await interaction.followup.send(content='*Вы состоите в полку?*', ephemeral=True,
                                                    view=view_squadron_buttons)
                else:
                    pass

                # await registration_functions.get_user_response(client, interaction)

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
