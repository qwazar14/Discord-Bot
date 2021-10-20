import bot.core.modules.utils.create_embed as create_embed


async def user_has_no_roles(ctx):
    await ctx.message.add_reaction('❌')
    return await create_embed.display_embed(ctx,
                                            f"{ctx.author} Title",
                                            "Description"
                                            )


async def user_send_invalid_argument():
    pass


async def command_doesnt_exist():
    pass
