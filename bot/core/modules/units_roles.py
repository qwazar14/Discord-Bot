from nextcord.ext import commands

# from bot.core.configs import roles_config
import bot.core.configs.roles_config as roles_config
from bot.core.configs.access_config import settings
from bot.core.modules.utils import clear_user_message

client = commands.Bot(command_prefix=settings['botPrefix'], help_command=None)


async def add_role_tank(ctx, user, guild_id):
    await clear_user_message.clear_last_user_message(ctx)
    await user.add_roles(guild_id.get_role(roles_config.unit_roles['tanks']))


async def add_role_plane(ctx, user, guild_id):
    await clear_user_message.clear_last_user_message(ctx)
    await user.add_roles(guild_id.get_role(roles_config.unit_roles['planes']))
