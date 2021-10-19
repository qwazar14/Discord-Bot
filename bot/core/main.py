import nextcord as discord
from nextcord.ext import commands
from PIL import Image, ImageDraw
import roles_config
from access_config import settings as settings


client = commands.Bot(command_prefix=settings['botPrefix'], help_command=None)


@client.event
async def on_ready():
    print('[LOG] Bot is ready!')


@client.command()
async def help(ctx):
    user = ctx.author
    print(f'[LOG] {user} called command "help"')
    await ctx.send("Custom help command")
    await ctx.message.add_reaction('✅')
    await ctx.message.delete(delay=5)
    print('[LOG] Help command done!')


@client.command()
async def tank(ctx):
    user = ctx.author
    print(f'[LOG] {user} called command "tank"')
    guild = client.get_guild(settings['guildId'])
    await user.add_roles(guild.get_role(roles_config.unit_roles['tanks']))
    await ctx.message.add_reaction('✅')
    await ctx.message.delete(delay=5)
    print('[LOG] Set role "Tank" command done!')


@client.command()
async def plane(ctx):
    user = ctx.author
    print(f'[LOG] {user} called command "plane"')
    guild = client.get_guild(settings['guildId'])
    await user.add_roles(guild.get_role(roles_config.unit_roles['planes']))
    await ctx.message.add_reaction('✅')
    await ctx.message.delete(delay=5)
    print('[LOG] Set role "Plane" command done!')


@client.command()
async def ship(ctx):
    user = ctx.author
    print(f'[LOG] {user} called command "ship"')
    guild = client.get_guild(settings['guildId'])
    await user.add_roles(guild.get_role(roles_config.unit_roles['ship']))
    await ctx.message.add_reaction('✅')
    await ctx.message.delete(delay=5)
    print('[LOG] Set role "Ship" command done!')


@client.command()
async def rules():
    pass


@commands.has_any_role(roles_config.discord_roles['admin'])
@client.command()
async def clear(ctx):
    user = ctx.author
    print(f'[LOG] {user} called command "clear"')
    pass


@client.command()
async def rb(ctx, nickname):
    user = ctx.author
    print(f'[LOG] {user} called command "rb"')
    link = "https://thunderskill.com/userbars/z/e/" + nickname + "/ru-1-combined-r.png"
    await ctx.send(link)
    print('[LOG] "rb" command done!')


@client.command()
async def sb(ctx, nickname):
    user = ctx.author
    print(f'[LOG] {user} called command "sb"')
    # driver = webdriver.Chrome()
    # driver.get(f"https://thunderskill.com/ru/stat/{nickname}")
    # button = driver.find_element_by_xpath('/html/body/div[3]/main/div/div/div/div[1]/div/button')
    # button.click()

    link = f"https://thunderskill.com/userbars/z/e/{nickname}/ru-1-combined-s.png"
    await ctx.send(link)

    print('[LOG] "sb" command done!')


@client.command()
async def card(ctx, user: discord.Member = None):
    guild = client.get_guild(settings['guildId'])
    size = (90,90,)
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)

    if user is None:
        user = ctx.author

    backgroundImage = Image.open(r'assets/images/background/resumeBackground.png')
    idraw = ImageDraw.Draw(backgroundImage)
    # await ctx.send(file=discord.File(fp=idraw, filename='card.png'))
    await ctx.send(file=discord.File(backgroundImage))
client.run(settings['botToken'])
