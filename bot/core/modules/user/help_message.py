from bot.core.modules.utils.message_transformation import clear_last_user_message


async def send_help_message(ctx):
    await clear_last_user_message(ctx)
    return await ctx.send("Custom help command")
