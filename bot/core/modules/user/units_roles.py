from nextcord.ext import commands

# from configs import roles_config
import configs.roles_config as roles_config
from configs.access_config import settings
from modules.utils.message_transformation import clear_last_user_message

client = commands.Bot(command_prefix=settings['botPrefix'], help_command=None)


async def add_role_tank(ctx, user, guild_id):
    await clear_last_user_message(ctx)
    await user.add_roles(guild_id.get_role(roles_config.unit_roles['tanks']))


async def add_role_plane(ctx, user, guild_id):
    await clear_last_user_message(ctx)
    await user.add_roles(guild_id.get_role(roles_config.unit_roles['planes']))
