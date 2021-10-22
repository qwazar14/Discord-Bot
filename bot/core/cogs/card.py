
import nextcord as discord

from nextcord.ext import commands
from nextcord.ext.commands.cog import Cog
from configs.access_config import settings
from modules.user import units_roles, parse_stats, card_generator


class Card(Cog):

    def __init__(self, client):
        self.client = client

    
    @commands.Cog.listener()
    async def tank(self, ctx):
        guild_id = self.client.get_guild(settings['guildId'])
        await units_roles.add_role_tank(ctx, ctx.author, guild_id)


    @commands.Cog.listener()
    async def plane(self, ctx):
        guild_id = self.client.get_guild(settings['guildId'])
        await units_roles.add_role_plane(ctx, ctx.author, guild_id)


    @commands.Cog.listener()
    async def rb(self, ctx, nickname: discord.Member = None):
        await self.parse_stats.get_statistics(ctx, nickname, 'r')


    @commands.Cog.listener()
    async def sb(ctx, nickname: discord.Member = None):
        await parse_stats.get_statistics(ctx, nickname, 's')


    @commands.Cog.listener()
    async def card(ctx, user: discord.Member = None):
        await card_generator.card(ctx, user, self.client)

def setup(bot):
    bot.add_cog(Card(bot))