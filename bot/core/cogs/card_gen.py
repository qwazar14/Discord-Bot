import io
import random

import nextcord as discord
from nextcord.ext import commands

from bot.core.configs import roles_config

from bot.core.configs.access_config import settings
from PIL import Image, ImageDraw, ImageFont, ImageOps

from bot.core.modules.utils import card_controller
from bot.core.modules.utils.card_controller import format_user_nickname, get_user_background_image


class CardGen(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def card(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        nickname = user.nick
        guild = self.client.get_guild(settings['guildId'])
        output = io.BytesIO()
        background_size = (1600, 1200)
        background_zone = (0, 0)

        # background_image = Image.open(r'assets/images/background/OF-1-3.png')
        background_image = await card_controller.get_background_image(self, user, self.client)
        card = background_image

        qrcode_image, qrcode_image_zone = await card_controller.get_user_qrcode(nickname)
        try:
            avatar, avatar_zone = await card_controller.get_user_avatar(self, user)
            card.paste(avatar, avatar_zone, avatar)
        except (AttributeError, TypeError) as e:
            pass

        user_image = await get_user_background_image(self, user, self.client)
        user_image_zone = (255, 190)
        card.paste(user_image, user_image_zone, user_image)

        await format_user_nickname(user, card)
        card.paste(background_image, background_zone, background_image)
        card.paste(qrcode_image, qrcode_image_zone, qrcode_image)

        card.save(output, "png")
        player_card = io.BytesIO(output.getvalue())
        return await ctx.send(file=discord.File(fp=player_card, filename='card.png'))


def setup(bot):
    bot.add_cog(CardGen(bot))
