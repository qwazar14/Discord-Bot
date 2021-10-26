import nextcord as discord
import nextcord

from nextcord.ext import commands

from bot.core.configs import roles_config


class Utils(commands.Cog):

    def __init__(self, client) -> None:
        super().__init__()
        self.client = client
        
    @commands.has_any_role(roles_config.discord_roles['admin'])    
    @commands.command()
    async def send_embed(self, ctx, title, *, text):
        embed=discord.Embed(title=title, color=0xe100ff)
        embed.set_thumbnail(url="https://i.imgur.com/mhSJtPm.png")
        embed.add_field(name="\u200b", value=text, inline=True)
        await ctx.send(embed=embed)
        await ctx.message.delete()

def setup(client):
    client.add_cog(Utils(client))