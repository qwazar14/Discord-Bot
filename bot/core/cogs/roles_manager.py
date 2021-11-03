from nextcord.ext import commands
from nextcord.ext.commands.cog import Cog

from configs.access_config import settings
from modules.user import member_roles


class RolesManager(Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def categories(self, ctx):
        guild_id = self.client.get_guild(settings['guildId'])
        await member_roles.add_util_categories(ctx, ctx.author, guild_id)


def setup(bot):
    bot.add_cog(RolesManager(bot))
