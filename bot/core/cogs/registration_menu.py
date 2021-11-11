import asyncio

import nextcord
import nextcord as discord
from nextcord.ext import commands

import modules.utils.ranks as rank_system

import modules.utils.registration_menu.registration_functions as registration_functions
from configs import roles_config
from configs.access_config import settings


class RegistrationMenu(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def registration_menu(self, ctx):
        class RegistrationMenuButtons(nextcord.ui.View):
            def __init__(self, client, *, timeout=None):
                super().__init__(timeout=timeout)
                self.client = client

            guild_id = self.client.get_guild(settings['guildId'])

            @discord.ui.button(label='Подать заявку в полк', style=nextcord.ButtonStyle.green)
            async def join_squadron(self, button, interaction, timeout_error_call=True, guild_id=guild_id):
                user = interaction.user
                await interaction.response.send_message(content='Введите ник в игре *(у вас есть 30 секунд)* ',
                                                        ephemeral=True)
                try:
                    nickname_user = await registration_functions.get_user_response(self.client, interaction)
                    await interaction.edit_original_message(content='Как Вас зовут? *(у вас есть 30 секунд)*')
                except asyncio.TimeoutError:
                    timeout_error_call = await registration_functions.timeout_error(interaction)

                if timeout_error_call is not False:
                    try:
                        name_user = await registration_functions.get_user_response(self.client, interaction)
                        await interaction.edit_original_message(
                            content='Введите ваш максимальный БР *(у вас есть 30 секунд)*')
                    except asyncio.TimeoutError:
                        timeout_error_call = await registration_functions.timeout_error(interaction)

                if timeout_error_call is not False:
                    try:
                        br_msg_content = await registration_functions.get_user_response(self.client, interaction)
                        try:
                            br_user = await registration_functions.replace_comma_to_do(br_msg_content)
                        except ValueError as ve:
                            await interaction.edit_original_message(
                                content='**Используйте только цифры! Начните заново**')
                            timeout_error_call = False
                        if timeout_error_call is not False:
                            if 1.0 <= br_user <= 11.0:
                                # if br_user
                                new_nickname = f"[{br_user}] {nickname_user} ({name_user})"
                            else:
                                await interaction.edit_original_message(
                                    content='**Боевой рейтинг может быть в диапазоне от 1.0 до 11.0. *Начните заново***')
                                timeout_error_call = False
                            if timeout_error_call is not False:
                                await interaction.edit_original_message(content='*Регистрация завершена*')
                                await user.edit(nick=new_nickname)
                                await user.add_roles(guild_id.get_role(roles_config.util_categories['rank_category']))
                                await user.add_roles(
                                    guild_id.get_role(roles_config.util_categories['unit_type_category']))
                                await user.add_roles(
                                    guild_id.get_role(roles_config.util_categories['optional_category']))
                                await user.add_roles(
                                    guild_id.get_role(roles_config.util_categories['general_category']))
                                await user.add_roles(guild_id.get_role(roles_config.unit_roles['planes']))
                                await user.add_roles(guild_id.get_role(roles_config.general_category_roles['player']))
                                await user.remove_roles(
                                    guild_id.get_role(roles_config.general_category_roles['new_player']))
                                await user.add_roles(guild_id.get_role(rank_system.get_rank_id_by_name('OR-1')))
                    except asyncio.TimeoutError:
                        await registration_functions.timeout_error(interaction)

            @discord.ui.button(label='Друг полка', style=nextcord.ButtonStyle.blurple)
            async def squadron_friend(self, button, interaction, timeout_error_call=True):
                user = interaction.user
                await interaction.response.send_message(content='Введите ник в игре *(у вас есть 30 секунд)* ',
                                                        ephemeral=True)
                try:
                    nickname_user = await registration_functions.get_user_response(self.client, interaction)
                    await interaction.edit_original_message(content='Как Вас зовут? *(у вас есть 30 секунд)*')
                except asyncio.TimeoutError:
                    timeout_error_call = await registration_functions.timeout_error(interaction)

                if timeout_error_call is not False:
                    try:
                        name_user = await registration_functions.get_user_response(self.client, interaction)
                    except asyncio.TimeoutError:
                        timeout_error_call = await registration_functions.timeout_error(interaction)

                    class SquadronMenu(nextcord.ui.View):
                        def __init__(self, client, *, timeout=None):
                            super().__init__(timeout=timeout)
                            self.client = client

                        @discord.ui.button(label='Да', style=nextcord.ButtonStyle.green)
                        async def get_user_squadron(self, button, interaction):
                            # await interaction.edit_original_message(content='*Введите клантег в формате XXXX')
                            await interaction.response.send_message(content='*Введите клантег в формате XXXX',
                                                                    ephemeral=True)
                            try:
                                squadron_user = await registration_functions.get_user_response(self.client, interaction)
                                if 5 >= len(squadron_user) > 1:
                                    new_nickname = f"[{squadron_user}] {nickname_user} ({name_user})"
                                    # await ctx.send()
                                    await user.edit(nick=new_nickname)
                                    await interaction.edit_original_message(content='*Регистрация завершена*')
                                else:
                                    await interaction.edit_original_message(
                                        content='**ОШИБКА** Клантег должен состоять максимум из 5 символов')
                            except asyncio.TimeoutError:
                                await registration_functions.timeout_error(interaction)

                        @discord.ui.button(label='Нет', style=nextcord.ButtonStyle.red)
                        async def end_user_registration(self, button, interaction):
                            new_nickname = f"[-] {nickname_user} ({name_user})"
                            # await ctx.send(new_nickname)
                            await user.edit(nick=new_nickname)
                            # await interaction.edit_original_message(content='*Регистрация завершена*')
                            await registration_functions.end_registration(self, interaction)

                    if timeout_error_call is not False:
                        view_squadron_buttons = SquadronMenu(self.client)
                        await interaction.edit_original_message(content='*Вы состоите в полку?*',
                                                                view=view_squadron_buttons)

        view = RegistrationMenuButtons(self.client)
        # rank = rank_system.get_member_rank(ctx.author, str=True)

        embed = discord.Embed(title="Вы попали на сервер полка GG Company",
                              description="**Если вы хотите вступить в полк, нажмите кнопку 'Подать заявку'**",
                              color=0xe100ff)
        embed.set_thumbnail(url="https://i.imgur.com/mhSJtPm.png")
        embed.add_field(name="Если вы зашли поиграть с друзьями, нажмите кнопку 'Друг полка'",
                        value="Нажимая кнопку вы автоматически соглашаетесь с правилами в канале <#877276991412379709>",
                        inline=False)

        message = await ctx.send(embed=embed, view=view)


def setup(bot):
    bot.add_cog(RegistrationMenu(bot))
