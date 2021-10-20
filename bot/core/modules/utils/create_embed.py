import nextcord as discord


async def display_embed(ctx, title, description):
    return await ctx.send(embed=discord.Embed(
        title=title,
        description=description,
        colour=discord.Colour.from_rgb(106, 192, 245)
    ))
