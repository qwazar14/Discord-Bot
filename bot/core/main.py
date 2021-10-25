import asyncio
import datetime
import os
import re

import nextcord
import nextcord as discord
from nextcord.ext import commands

import modules.utils.error_controller as error_controller
import modules.utils.message_transformation as message_transformation
import modules.utils.ranks as rank_system
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


@client.command()
async def registration_menu(ctx):
    class RegistrationMenu(nextcord.ui.View):

        @discord.ui.button(label='Подать заявку', style=nextcord.ButtonStyle.green)
        async def registration(self, button, interaction):
            await interaction.response.send_message(content='Введите ник в игре', ephemeral=True)
            # await interaction.response.send_message(content='Как Вас зовут?', ephemeral=True)
            # await interaction.response.send_message(content='Какой максимальный БР?', ephemeral=True)
            self.clear_items()
            embed = message.embeds[0]
            # embed.color = 0x38a22a
            # embed.title = 'Принято'
            await message.edit(embed=embed, view=self)
            self.stop()

        @discord.ui.button(label='Друг полка', style=nextcord.ButtonStyle.blurple)
        async def squadron_friend(self, button, interaction):
            await interaction.response.send_message(content='Введите ник в игре', ephemeral=True)
            try:
                msg_id_group = await client.wait_for("message", timeout=30)  # 30 seconds to reply

                # print(f"msgid_group\n{msg_id_group}")
                msg_id = int(re.search(r"[0-9]+", str(msg_id_group)).group(0).strip())

                async def get_message_text(msg_id1):
                    return await ctx.fetch_message(int(msg_id1))

                # print(f"msgid\n{msg_id}")

                msg_text = await get_message_text(msg_id)
                await ctx.send(msg_id)


            except asyncio.TimeoutError:
                await ctx.send("Sorry, you didn't reply in time!")

            # await interaction.response.send_message(content='Как Вас зовут?', ephemeral=True)
            # await interaction.response.send_message(content='Введите ваш клантег(Если есть) *например: PVVD*',
            #                                         ephemeral=True)

            self.clear_items()
            embed = message.embeds[0]
            # embed.color = 0xde3b3b
            # embed.title = 'Отказ'
            await message.edit(embed=embed, view=self)
            self.stop()

    view = RegistrationMenu()
    rank = rank_system.get_member_rank(ctx.author, str=True)
    print(f'RAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANK: {rank}')
    now = datetime.datetime.now(datetime.timezone.utc)

    # if rank in ['OF-8', 'OF-9', 'OF-10']:
    #     await ctx.author.send(
    #         'Вы заняли максимальное звание в нашем полке. Подача заявки на повышение для вас закрыта.')
    #     return

    timedelta = now - ctx.author.joined_at
    seconds = timedelta.total_seconds()
    days = seconds // 86400
    month = days // 30
    days = days - (month * 30)

    datestr = f'{int(month)} месяцев и {int(days)} дней'
    embed = discord.Embed(title="Вы попали на сервер полка GG Company",
                          description="**Если вы хотите вступить в полк, нажмите кнопку 'Подать заявку'**",
                          color=0xe100ff)
    embed.set_thumbnail(url="https://i.imgur.com/mhSJtPm.png")
    embed.add_field(name="Если вы зашли поиграть с друзьями, нажмите кнопку 'Друг полка'",
                    value="Нажимая кнопку вы автоматически соглашаетесь с правилами в канале <#877276991412379709>",
                    inline=False)

    message = await ctx.send(embed=embed, view=view)


@client.command()
async def up(ctx):
    class RankSys(nextcord.ui.View):

        @discord.ui.button(label='Повысить', style=nextcord.ButtonStyle.green)
        async def rank_up(self, button, interaction):
            new_rank = rank_system.get_next_member_rank(ctx.author)
            if interaction.user == ctx.author:
                await interaction.response.send_message(content='Вы не можете повысить самого себя!', ephemeral=True)
                return
            if new_rank in rank_system.get_officers_ranks_id():
                if not rank_system.if_member_can_up_officers(interaction.user):
                    await interaction.response.send_message(content='Вы не можете повышать офицеров!', ephemeral=True)
                    return
            if not rank_system.if_rank_member1_above_member2(ctx.author, interaction.user):
                await interaction.response.send_message(
                    content='Вы не можете повышать игроков, у которых ранг выше вашего!', ephemeral=True)
                return
            await ctx.author.remove_roles(ctx.guild.get_role(rank_system.get_rank_id_by_name(rank)))
            await ctx.author.add_roles(ctx.guild.get_role(new_rank))
            await ctx.author.send('Ваc повысили.')
            self.clear_items()
            embed = message.embeds[0]
            embed.color = 0x38a22a
            embed.title = 'Принято'
            await message.edit(embed=embed, view=self)
            self.stop()

        @discord.ui.button(label='Отказ', style=nextcord.ButtonStyle.red)
        async def deny(self, button, interaction):
            if interaction.user == ctx.author:
                await interaction.response.send_message(content='Вы не можете повысить самого себя!', ephemeral=True)
                return
            if not rank_system.if_member_can_up_officers(interaction.user):
                await interaction.response.send_message(content='Вы не можете повышать офицеров!', ephemeral=True)
                return
            if not rank_system.if_rank_member1_above_member2(interaction.user, ctx.author):
                await interaction.response.send_message(
                    content='Вы не можете повышать игроков, у которых ранг выше вашего!', ephemeral=True)
                return
            await ctx.author.send('Вам отказали в повышение. Следующий запрос возможен через неделю.')
            self.clear_items()
            embed = message.embeds[0]
            embed.color = 0xde3b3b
            embed.title = 'Отказ'
            await message.edit(embed=embed, view=self)
            self.stop()

    view = RankSys()
    rank = rank_system.get_member_rank(ctx.author, str=True)
    print(f'RAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANK: {rank}')
    now = datetime.datetime.now(datetime.timezone.utc)

    if rank in ['OF-8', 'OF-9', 'OF-10']:
        await ctx.author.send(
            'Вы заняли максимальное звание в нашем полке. Подача заявки на повышение для вас закрыта.')
        return

    timedelta = now - ctx.author.joined_at
    seconds = timedelta.total_seconds()
    days = seconds // 86400
    month = days // 30
    days = days - (month * 30)

    datestr = f'{int(month)} месяцев и {int(days)} дней'

    embed = discord.Embed(title="Запрос на повышение", color=0xf2930d)
    embed.add_field(name=f"Игрок {ctx.author.nick} запрашивает повышение.", value=f"Текущее звание: {rank}",
                    inline=True)
    embed.set_footer(text=f"На сервере {datestr}")
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
