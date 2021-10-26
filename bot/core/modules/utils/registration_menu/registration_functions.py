# import asyncio


async def timeout_error(interaction):
    await interaction.followup.send(content='*Извините, вы не ответили вовремя! Повторите попытку*', ephemeral=True)
    return False


async def get_user_response(client, interaction):
    msg = await client.wait_for("message", timeout=5, check=lambda
        m: m.author == interaction.user and m.channel == interaction.channel)
    return msg.content


async def replace_comma_to_do(br_msg_content):
    replaced_message = max([float(i) for i in br_msg_content.replace(',', '.').split()])
    return replaced_message
