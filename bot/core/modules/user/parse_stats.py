import re
import response as response

from bot.core.modules.utils import clear_user_message
import requests


async def get_statistics(ctx, nickname, mode):
    await clear_user_message.clear_last_user_message(ctx)
    if nickname is None:
        nickname = ctx.author.nick
    # Git позязя заработай
    nickname = re.search("(?<=\])(.*?)(?=\()", nickname).group(0).strip()
    link = f"https://thunderskill.com/userbars/z/e/{nickname}/ru-1-combined-{mode}.png"
    response_link = requests.get(link)
    if response_link.status_code == 200:
        print(response_link)
        return await ctx.send(link)
    elif response_link.status_code == 404:
        return await ctx.send(f"Error {response_link.status_code}")
    else:
        return await ctx.send(response_link.status_code)