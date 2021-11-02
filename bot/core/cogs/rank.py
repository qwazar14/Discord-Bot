
import datetime
import nextcord as discord
import nextcord
from nextcord.components import SelectOption
from nextcord.ext import commands
from nextcord.ui import view

import modules.utils.ranks as RankSystem


class RankManager(commands.Cog):

    def __init__(self, client) -> None:
        self.client = client

    @commands.command()
    async def down(self, ctx, user: discord.Member):

        class View(nextcord.ui.View):
            
            @discord.ui.select(placeholder='Выберите ранг', min_values=1, max_values=1, options=[SelectOption(label="Lol"),SelectOption(label="Kek")])
            async def select_rank(self, select, interaction):
                self.down_rank = select.values[0]

            @discord.ui.button(label = 'Потвердить', style = nextcord.ButtonStyle.red)
            async def confirm(self, button, interaction):
                '''if interaction.user == ctx.author:
                    await interaction.response.send_message(content='Вы не можете понизить самого себя!',ephemeral=True)   
                    return
                if not RankSystem.if_member_can_up_officers(interaction.user):
                    await interaction.response.send_message(content='Вы не можете понижать офицеров!',ephemeral=True)   
                    return
                if not RankSystem.if_rank_member1_above_member2(interaction.user, ctx.author):
                    await interaction.response.send_message(content='Вы не можете понижать игроков, у которых ранг выше вашего!',ephemeral=True)   
                    return'''
                await ctx.author.remove_roles(ctx.guild.get_role(RankSystem.get_rank_id_by_name(user_rank)))
                await ctx.author.add_roles(ctx.guild.get_role(RankSystem.get_rank_id_by_name(self.down_rank)))
                await ctx.author.send(f'Ваc позизили в ранге до {self.down_rank}.')
                self.clear_items()
                embed = message.embeds[0]
                embed.color = 0xC03537
                embed.title = 'Потверждение'
                embed.add_field(name='Понижен:', value=interaction.user.mention+f'\n||{interaction.user}||', inline=False)
                await message.edit(embed=embed,view=self)
                self.stop()
                

            @discord.ui.button(label = 'Отмена', style = nextcord.ButtonStyle.grey)
            async def cancel(self, button, interaction):
                await message.delete()

        view = View()
        

        rank_list = []
        user_rank = RankSystem.get_member_rank(user, str=True)
        ranks = RankSystem.get_all_ranks_name()
        index = ranks.index(user_rank)-1
        embed=discord.Embed(title="Понижение", color=0xf2930d)
        embed.add_field(name=f"Вы собираетесь понизить {ctx.author.nick} в ранге", value=f"Ранг на момент понижения: {user_rank}\n\nУпоминание: {ctx.author.mention}", inline=True)

        for i in range(index,-1,-1):
            rank_list.append(SelectOption(label=ranks[i]))
        
        view.children[0].options = rank_list

        message = await ctx.send(embed=embed, view=view)


        


    @commands.command()
    async def up(self, ctx):
        
        class View(nextcord.ui.View):
        
            @discord.ui.button(label = 'Повысить', style = nextcord.ButtonStyle.green)
            async def rank_up(self, button, interaction):
                new_rank = RankSystem.get_next_member_rank(ctx.author)
                if interaction.user == ctx.author:
                    await interaction.response.send_message(content='Вы не можете повысить самого себя!',ephemeral=True)   
                    return
                if new_rank in RankSystem.get_officers_ranks_id():
                    if not RankSystem.if_member_can_up_officers(interaction.user):
                        await interaction.response.send_message(content='Вы не можете повышать офицеров!',ephemeral=True)   
                        return
                if not RankSystem.if_rank_member1_above_member2(ctx.author, interaction.user):
                    await interaction.response.send_message(content='Вы не можете повышать игроков, у которых ранг выше вашего!',ephemeral=True)   
                    return
                await ctx.author.remove_roles(ctx.guild.get_role(RankSystem.get_rank_id_by_name(rank)))
                await ctx.author.add_roles(ctx.guild.get_role(new_rank))
                await ctx.author.send('Ваc повысили.')
                self.clear_items()
                embed = message.embeds[0]
                embed.color = 0x38a22a
                embed.title = 'Принято' 
                embed.add_field(name='Повышен:', value=interaction.user.mention+f'\n||{interaction.user}||', inline=False)
                await message.edit(embed=embed,view=self)
                self.stop()

            @discord.ui.button(label = 'Отказ', style = nextcord.ButtonStyle.red)
            async def deny(self, button, interaction):
                if interaction.user == ctx.author:
                    await interaction.response.send_message(content='Вы не можете повысить самого себя!',ephemeral=True)   
                    return
                if not RankSystem.if_member_can_up_officers(interaction.user):
                    await interaction.response.send_message(content='Вы не можете повышать офицеров!',ephemeral=True)   
                    return
                if not RankSystem.if_rank_member1_above_member2(interaction.user, ctx.author):
                    await interaction.response.send_message(content='Вы не можете повышать игроков, у которых ранг выше вашего!',ephemeral=True)   
                    return
                await ctx.author.send('Вам отказали в повышение. Следующий запрос возможен через неделю.')
                self.clear_items()
                embed = message.embeds[0]
                embed.color = 0xde3b3b
                embed.title = 'Отказ'
                await message.edit(embed=embed,view=self)
                self.stop()

            


        view = View()
        rank = RankSystem.get_member_rank(ctx.author, str=True)
        now = datetime.datetime.now(datetime.timezone.utc)

        if rank in ['OF-8','OF-9','OF-10']:
            await ctx.author.send('Вы заняли максимальное ранг в нашем полке. Подача заявки на повышение для вас закрыта.')
            return
        
        timedelta = now - ctx.author.joined_at
        seconds = timedelta.total_seconds()
        days = seconds // 86400
        month = days // 30
        days = days - (month * 30)

        datestr = f'{int(month)} месяцев и {int(days)} дней'

        embed=discord.Embed(title="Запрос на повышение", color=0xf2930d)
        embed.add_field(name=f"Игрок {ctx.author.nick} запрашивает повышение.", value=f"Ранг на момент подачи заявки: {rank}\n\nУпоминание: {ctx.author.mention}", inline=True)
        embed.set_footer(text=f"На сервере {datestr}")
        message = await ctx.send(embed=embed, view=view)

def setup(client):
    client.add_cog(RankManager(client))