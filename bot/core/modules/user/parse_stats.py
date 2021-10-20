import re
from bot.core.modules.utils import clear_user_message


async def get_statistics(ctx, nickname, mode):
    await clear_user_message.clear_last_user_message(ctx)
    if nickname is None:
        nickname = ctx.author
    nickname = re.search(r"(?<=\])(.*?)(?=\()", nickname).strip()

    link = f"https://thunderskill.com/userbars/z/e/{nickname}/ru-1-combined-{mode}.png"
    print(link)
    return await ctx.send(link)
