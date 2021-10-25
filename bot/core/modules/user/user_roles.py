from nextcord.ext import commands

# from configs import roles_config
import bot.core.configs.roles_config as roles_config
from bot.core.configs.access_config import settings

client = commands.Bot(command_prefix=settings['botPrefix'], help_command=None)


async def add_util_categories(ctx, user, guild_id):
    # await clear_last_user_message(ctx)
    await user.add_roles(guild_id.get_role(roles_config.util_categories['rank_category']))
    await user.add_roles(guild_id.get_role(roles_config.util_categories['unit_type_category']))
    await user.add_roles(guild_id.get_role(roles_config.util_categories['optional_category']))
    await user.add_roles(guild_id.get_role(roles_config.util_categories['general_category']))
    await user.add_roles(guild_id.get_role(roles_config.general_category_roles['player']))


async def new_player_joined(user, guild_id):
    await user.add_roles(guild_id.get_role(roles_config.util_categories['general_category']))
    await user.add_roles(guild_id.get_role(roles_config.general_category_roles['new_player']))
#     role = nextcord.utils.get(user.guild.roles, name='Имя роли') # САМА РОЛЬ КОТОРУЮ ВЫДАЕМ
#     await member.add_roles(role) # ДОБАВЛЯЕМ РОЛЬ
