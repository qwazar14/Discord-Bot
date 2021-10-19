async def clear_last_user_message(ctx):
    delete_delay = 5  # seconds
    await ctx.message.add_reaction('✅')
    await ctx.message.delete(delay=delete_delay)
    return print("[LOG]: Cleared last user message")
