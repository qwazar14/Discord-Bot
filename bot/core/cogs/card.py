import nextcord as discord
from nextcord.ext import commands


from bot.core.configs.access_config import settings
from bot.core.modules.user import units_roles, parse_stats, card_generator


class Card(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command()
    async def tank(self, ctx):
        guild_id = self.client.get_guild(settings['guildId'])
        await units_roles.add_role_tank(ctx, ctx.author, guild_id)


    @commands.command()
    async def plane(self, ctx):
        guild_id = self.client.get_guild(settings['guildId'])
        await units_roles.add_role_plane(ctx, ctx.author, guild_id)


    @commands.command()
    async def rb(self, ctx, nickname: discord.Member = None):
        await parse_stats.get_statistics(ctx, nickname, 'r')

    @commands.command()

    async def sb(self, ctx, nickname: discord.Member = None):
        await parse_stats.get_statistics(ctx, nickname, 's')

    @commands.command()
    async def card(self, ctx, user: discord.Member = None):
        await card_generator.card(ctx, user, self.client)


def setup(bot):
    bot.add_cog(Card(bot))
