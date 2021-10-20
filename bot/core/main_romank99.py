import nextcord as discord
from nextcord.ext import commands

import roles_config
from access_config import settings as settings

client = commands.Bot(command_prefix=settings['botPrefix'], help_command=None)


@client.event
async def on_ready():
    print('[LOG] Bot is ready!')


class Roles(discord.ui.View):
    def __init__(self):
        self.value = None

    @discord.ui.button(label = 'Plane', style=discord.ButtonStyle.green)
    async def Plane(self, button: discord.ui.Button, interaction: discord.Interaction):
        user = discord.author
        guild = client.get_guild(settings['guildId'])
        await user.add_roles(guild.get_role(roles_config.unit_roles['planes']))
        await interaction.response.send_message('You are GAY', ephemeral=True)
        self.value = True
       
        


    @discord.ui.button(label = 'Tank', style=discord.ButtonStyle.red)
    async def Tank(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message('You are ground GAY', ephemeral=True)
        self.value = True
        self.stop()
        

@client.command()
async def sub(ctx):
    view = Roles()
    await ctx.send('Are You?', view=view)
    await view.wait()



@client.command()
async def help(ctx):
    user = ctx.author
    print(f'[LOG] {user} called command "help"')
    embed = discord.Embed(color = 0x9900, title = "Custom help command")
    embed.set_author(name = ctx.author.display_name, icon_url= ctx.author.avatar.url)
    embed.set_thumbnail(url="https://avatars.mds.yandex.net/i?id=2a00000179f8985e845048ef5412f9930614-5175033-images-thumbs&n=13")
    embed.add_field(name="Список доступных комманд", value = "Для просмотра существующих ролей введите - !roles \nДля того, чтобы получить инфаркт от вашей статки введите - !stats", inline=False)
    await ctx.send(embed = embed)
    view = Roles()
    await ctx.send('subcribe?', view=view)
    await view.wait()
    await ctx.message.add_reaction('✅')
    await ctx.message.delete(delay=5)
    print('[LOG] Help command done!')


@client.command()
async def roles(ctx):
    user = ctx.author
    print(f'[LOG] {user} called command "roles"')
    embed = discord.Embed(color = 0x9900, title = "Custom roles command \nВыберите роль: \n !tank \n !plane \n !ship")
    await ctx.send(embed = embed)
    await ctx.message.add_reaction('✅')
    await ctx.message.delete(delay=5)
    print('[LOG] Roles command done!')

@client.command()
async def stats(ctx):
    user = ctx.author
    print(f'[LOG] {user} called command "stats"')
    await ctx.send("Custom stats command \nВыберите режим: \n !tank \n !plane \n !ship")
    await ctx.message.add_reaction('✅')
    await ctx.message.delete(delay=5)
    print('[LOG] Stats command done!')


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
    link = "https://thunderskill.com/userbars/z/e/" + \
        nickname + "/ru-1-combined-r.png"
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
async def test(ctx):
    pass

client.run(settings['botToken'])
