import re
from modules.utils import clear_user_message


async def get_statistics(ctx, nickname, mode):
    await clear_user_message.clear_last_user_message(ctx)
    if nickname is None:
        nickname = ctx.author.nick
    nickname = re.search("(?<=\])(.*?)(?=\()", nickname).group(0).strip()
    link = f"https://thunderskill.com/userbars/z/e/{nickname}/ru-1-combined-{mode}.png"
    print(link)
    return await ctx.send(link)
