import nextcord
from bot.core.configs.util_config import registration_menu


async def timeout_error(interaction):
    await interaction.followup.send(content='*Извините, вы не ответили вовремя! Повторите попытку*', ephemeral=True)
    return False


async def get_user_response(client, interaction):
    msg = await client.wait_for("message", timeout=registration_menu['timeout'], check=lambda
        m: m.author == interaction.user and m.channel == interaction.channel)
    return msg.content


async def replace_comma_to_do(br_msg_content):
    replaced_message = max([float(i) for i in br_msg_content.replace(',', '.').split()])
    return replaced_message


async def end_registration(self, interaction):
    await interaction.response.send_message(content='*Регистрация завершена*', ephemeral=True)
    return False


# class SquadronMenu(nextcord.ui.View):
#
#     @nextcord.ui.button(label='Да', style=nextcord.ButtonStyle.green)
#     async def squadron_friend1(self, button, interaction):
#         await interaction.response.send_message(content='*Введите клантег полка(например*', ephemeral=True)
#
#
#     @nextcord.ui.button(label='Нет', style=nextcord.ButtonStyle.red)
#     async def squadron_friend2(self, button, interaction):
#         await interaction.response.send_message(content='*Регистрация завершена*', ephemeral=True)
#         return False
