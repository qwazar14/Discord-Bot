import modules.utils.clear_user_message as clear_user_message


async def send_help_message(ctx):
    await clear_user_message.clear_last_user_message(ctx)
    return await ctx.send("Custom help command")
