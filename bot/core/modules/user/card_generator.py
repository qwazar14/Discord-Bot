import io

import nextcord as discord
import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps

import configs.roles_config as roles_config
from configs.access_config import settings as settings


async def card(ctx, user, client):
    guild = client.get_guild(settings['guildId'])
    output = io.BytesIO()

    if user is None:
        user = ctx.author
    medal_zone = Image.new('RGBA', (850, 200), (0, 0, 0, 0))
    # image_size = (800, 600)
    background_zone = (0, 0)
    # grad = Image.new('RGBA', image_size)
    background = Image.open(r'assets/images/background/resumeBackground.png')
    background.paste(background, background_zone, background)

    try:
        avatar_size = (100, 100,)
        avatar_zone = (151, 37)
        avatar_mask = Image.new('L', avatar_size, 0)
        avatar_draw = ImageDraw.Draw(avatar_mask)
        avatar_draw.rectangle((0, 0) + avatar_size, fill=255)
        avatar_url = str(user.avatar.url)
        resp = requests.get(avatar_url, stream=True)
        resp = Image.open(io.BytesIO(resp.content))
        resp = resp.convert('RGBA')
        # resp = resp.resize((90, 90), Image.ANTIALIAS)
        avatar = ImageOps.fit(resp, avatar_mask.size)
        avatar.putalpha(avatar_mask)
        background.paste(avatar, avatar_zone, avatar)
    except AttributeError as error:
        pass

    user_id = str(user.id)
    font = ImageFont.truetype("arialbd.ttf", 32, encoding="unic")  # X435, Y300 text

    user_id_text_zone = (435, 25)
    user_name_text_zone = (348, 57)
    rgb_black = (0, 0, 0)
    user_id_text_draw = ImageDraw.Draw(background)
    user_id_text_draw.text(user_id_text_zone, user_id[13:18], rgb_black, font=font)

    user_name = f'{user.nick}'
    user_name = user_name.split(']')
    user_name = user_name[1].split('(')
    user_name = user_name[0]

    user_name_text_draw = ImageDraw.Draw(background)
    user_name_text_draw.text(user_name_text_zone, user_name, rgb_black, font=font)

    user_units_zone = (474, 88)

    if guild.get_role(roles_config.unit_roles['tanks']) and guild.get_role(
            roles_config.unit_roles['planes']) in user.roles:
        user_has_both_roles = ImageDraw.Draw(background)
        user_has_both_roles.text(user_units_zone, "УНИВЕРСАЛ", rgb_black, font=font)
    elif guild.get_role(roles_config.unit_roles['tanks']) in user.roles:
        user_has_tank_role = ImageDraw.Draw(background)
        user_has_tank_role.text(user_units_zone, "НАЗЕМНЫЕ", rgb_black, font=font)
    elif guild.get_role(roles_config.unit_roles['planes']) in user.roles:
        user_has_plane_role = ImageDraw.Draw(background)
        user_has_plane_role.text(user_units_zone, "ВОЗДУШНЫЕ", rgb_black, font=font)
    else:
        user_has_no_roles = ImageDraw.Draw(background)
        user_has_no_roles.text(user_units_zone, "СЕКРЕТНО", rgb_black, font=font)
    background.save(output, "png")
    player_card = io.BytesIO(output.getvalue())
    return await ctx.send(file=discord.File(fp=player_card, filename='card.png'))
