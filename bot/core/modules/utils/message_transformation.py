import nextcord


# from modules.utils import clear_user_message


async def clear_some_messages(ctx, amount):
    await clear_last_user_message(ctx)
    await ctx.channel.purge(limit=int(amount) + 1)


async def send_embed_to_the_channel_as_bot(ctx):
    embed_var = nextcord.Embed(title=ctx, description="Desc", color=0x00ff00)
    embed_var.add_field(name="Field1", value="hi", inline=False)
    embed_var.add_field(name="Field2", value="hi2", inline=False)
    await ctx.channel.send(embed=embed_var)


async def send_rules_to_the_channel(ctx):
    embed_var = nextcord.Embed(title="Rules", description="Desc", color=0x00ff00)
    embed_var.add_field(name="Field1", value="hi", inline=False)
    embed_var.add_field(name="Field2", value="hi2", inline=False)
    await ctx.channel.send(embed=embed_var)


async def clear_last_user_message(ctx):
    delete_delay = 5  # seconds
    await ctx.message.add_reaction('✅')
    await ctx.message.delete(delay=delete_delay)
    print("[LOG]: Cleared last user message")
