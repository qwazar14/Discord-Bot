from bot.core.modules.utils import clear_user_message


async def get_statistics(ctx, nickname, mode):
    await clear_user_message.clear_last_user_message(ctx)
    if nickname is None:
        nickname = ctx.author
    nickname = f'{nickname.nick}'
    nickname = nickname.split('] ')
    nickname = nickname[1].split(' (')
    nickname = nickname[0]
    print(nickname)
    link = f"https://thunderskill.com/userbars/z/e/{nickname}/ru-1-combined-{mode}.png"
    return await ctx.send(link)
