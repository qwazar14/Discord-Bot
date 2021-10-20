import bot.core.modules.utils.create_embed as create_embed


async def user_has_no_roles(ctx):
    user = ctx.author
    await ctx.message.add_reaction('❌')
    await ctx.send(f"||{user.mention}||")
    await create_embed.display_embed(ctx,
                                     f"Role Error",
                                     f"{user.mention} has no roles"
                                     )


async def user_send_invalid_argument():
    pass


async def command_doesnt_exist():
    pass
