import asyncio

import nextcord
import nextcord as discord
from nextcord.ext import commands

import core.modules.utils.ranks as rank_system
import core.modules.utils.registration_menu.registration_functions as registration_functions
from core.configs import roles_config


class RegistrationMenu(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def registration_menu(self, ctx):
        class RegistrationMenuButtons(nextcord.ui.View):
            def __init__(self, client, *, timeout=None):
                super().__init__(timeout=timeout)
                self.BR_MIN = 1.0
                self.BR_MAX = 11.3
                self.client = client

            guild_id = self.client.guilds[0]

            # Подать заявку в полк start
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
                        except ValueError as e:
                            await interaction.edit_original_message(
                                content='**Используйте только цифры! Начните заново**')
                            timeout_error_call = False
                        if timeout_error_call is not False:
                            if self.BR_MIN <= br_user <= self.BR_MAX:
                                # if br_user
                                new_nickname = f"[{br_user}] {nickname_user} ({name_user})"
                            else:
                                await interaction.edit_original_message(
                                    content=f'**Боевой рейтинг может быть в диапазоне от {self.BR_MIN} до {self.BR_MAX}. *Начните заново***')
                                timeout_error_call = False
                            if timeout_error_call is not False:
                                await interaction.edit_original_message(content='*Регистрация завершена*')
                                await user.edit(nick=new_nickname)
                                await user.add_roles(guild_id.get_role(roles_config.util_categories['rank_category']))
                                await user.add_roles(
                                    guild_id.get_role(roles_config.util_categories['optional_category']))
                                await user.add_roles(
                                    guild_id.get_role(roles_config.util_categories['general_category']))
                                await user.add_roles(
                                    guild_id.get_role(roles_config.optional_category_roles['warthunder']))
                                await user.add_roles(guild_id.get_role(roles_config.general_category_roles['player']))
                                await user.remove_roles(
                                    guild_id.get_role(roles_config.general_category_roles['new_player']))
                                await user.add_roles(guild_id.get_role(rank_system.get_rank_id_by_name('OR-1')))
                    except asyncio.TimeoutError:
                        await registration_functions.timeout_error(interaction)

            # Подать заявку в полк end

            # Друг полка start
            @discord.ui.button(label='Друг полка', style=nextcord.ButtonStyle.blurple)
            async def squadron_friend(self, interaction, timeout_error_call=True, guild_id=guild_id):
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
                                    await user.add_roles(
                                        guild_id.get_role(roles_config.util_categories['optional_category']))
                                    await user.add_roles(guild_id.get_role(907975449798406216))
                                    await user.add_roles(
                                        guild_id.get_role(roles_config.util_categories['general_category']))
                                    await user.add_roles(
                                        guild_id.get_role(roles_config.optional_category_roles['warthunder']))
                                    await user.add_roles(
                                        guild_id.get_role(roles_config.general_category_roles['player']))
                                    await user.remove_roles(
                                        guild_id.get_role(roles_config.general_category_roles['new_player']))
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
                            await user.add_roles(
                                guild_id.get_role(roles_config.util_categories['optional_category']))
                            await user.add_roles(guild_id.get_role(907975449798406216))
                            await user.add_roles(
                                guild_id.get_role(roles_config.util_categories['general_category']))
                            await user.add_roles(
                                guild_id.get_role(roles_config.optional_category_roles['warthunder']))
                            await user.add_roles(
                                guild_id.get_role(roles_config.general_category_roles['player']))
                            await user.remove_roles(
                                guild_id.get_role(roles_config.general_category_roles['new_player']))
                            await interaction.edit_original_message(content='*Регистрация завершена*')

                    if timeout_error_call is not False:
                        view_squadron_buttons = SquadronMenu(self.client)
                        await interaction.edit_original_message(content='*Вы состоите в полку?*',
                                                                view=view_squadron_buttons)
            # Друг полка end

        view = RegistrationMenuButtons(self.client)
        # rank = rank_system.get_member_rank(ctx.author, str=True)

        embed = discord.Embed(title="Вы попали на сервер полка GG Company",
                              description="**Если вы хотите вступить в полк, нажмите кнопку 'Подать заявку'**",
                              color=0xe100ff)
        embed.set_thumbnail(url="https://i.imgur.com/mhSJtPm.png")
        embed.add_field(name="Если вы зашли поиграть с друзьями, нажмите кнопку 'Друг полка'",
                        value="Нажимая кнопку вы автоматически соглашаетесь с правилами в канале <#877276991412379709>",
                        inline=False)
        await ctx.send(embed=embed, view=view)


def setup(bot):
    bot.add_cog(RegistrationMenu(bot))
