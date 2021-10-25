from itertools import count
import nextcord as discord
import pymysql
import pymysql.cursors
import time
import datetime
import re
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from configs.bd_config import CONFIG
from configs.access_config import settings as access_config
from configs import roles_config
from nextcord.ext import commands, tasks
from nextcord.utils import get
from datetime import datetime, timedelta

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.con = pymysql.connect(
                      host=CONFIG['host'],
                      user=CONFIG['user'],
                      password=CONFIG['password'],
                      database=CONFIG['db'])

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author == self.bot.user: 
            return  

        counter = 0
        async for check_message in message.channel.history(limit=10):
            if check_message.author == message.author and not check_message.author.bot:
                if check_message.content == message.content and message.content[0] != access_config['botPrefix']:
                    counter += 1
        if counter >= 3:
            async for check_message in message.channel.history(limit=10):
                if check_message.author == message.author:
                    await check_message.delete()
            with self.con.cursor() as cursor:
                id = datetime.now().timestamp()
                cursor.execute(f"INSERT INTO `WarnsDB` (`id`, `gid`, `uid`, `w_reason`, `w_by`, `w_time`) VALUES ('{id}', '{message.author.guild.id}', '{message.author.id}', 'Спам', '{self.bot.user.id}', '{time.strftime('%b %d %Y')}')")
            self.con.commit()
            embed = discord.Embed (
                description=f"{message.author} получил предупреждение | Причина: Спам", 
                color = 0xe871ff
                )
            await message.channel.send(embed=embed)
            emb = discord.Embed (
                title=f"Сервер {message.author.guild}", 
                description=f"Вы получили предупреждение | Причина: Спам", 
                color = 0xe871ff
                )
            await message.author.send(embed=emb)


    @commands.command(
        usage="clear [лимит]",
        description="Очистить сообщения",
        brief="clear 10"
        )
    @commands.has_any_role(roles_config.discord_roles['admin'])
    async def clear(self, ctx, limit: int):
        try:
            await ctx.channel.purge(limit=limit+1)
            embed = discord.Embed (
                description=f"Очищено {limit} сообщ.", 
                color = 0xe871ff
                )
            await ctx.send (embed=embed, delete_after=4 )
        except:
            embed = discord.Embed (
                title=f"Ошибка доступа!", 
                description=f"У меня нету прав на удаление сообщений!", 
                color = ctx.author.color
                )
            await ctx.send (embed=embed, delete_after=4)

    @commands.command(
        usage="warn <пользователь> (причина)",
        description="Выдать предупреждение пользователю",
        brief="warn @M1racle Оскорбление"
        )
    @commands.has_any_role(roles_config.discord_roles['admin'])
    async def warn (self, ctx, user: discord.Member, *, reason = None):
        with self.con.cursor() as cursor:
            cursor.execute(f"INSERT INTO `WarnsDB` (`gid`, `uid`, `w_reason`, `w_by`, `w_time`) VALUES ('{ctx.guild.id}', '{user.id}', '{reason}', '{ctx.author}', '{time.strftime('%b %d %Y')}')")
        self.con.commit()
        embed = discord.Embed (
            description=f"✅ | Участник {user} получил предупреждение | Причина: {reason}", 
            color = 0xe871ff
            )
        await ctx.send(embed=embed)
        emb = discord.Embed (
            title=f"Сервер {ctx.guild.name}", 
            description=f"Вы получили предупреждение | Причина: {reason}", 
            color = 0xe871ff
            )
        await user.send (embed=emb)

    @commands.command(
        usage="remwarn [ID предупреждения]",
        description="Снять предупреждение пользователю",
        brief="remwarn 103473158"
        )
    @commands.has_any_role(roles_config.discord_roles['admin'])
    async def remwarn(self, ctx, id: int):
        with self.con.cursor() as cursor:
            cursor.execute("SELECT gid, uid FROM `WarnsDB` WHERE `gid`=%s AND `id`=%s", (ctx.guild.id, id))
            if cursor.fetchone() == None:
                embed = discord.Embed (
                    description=f"Данного ID нету в базе!", 
                    color = ctx.author.color
                )
                await ctx.send (embed=embed)
            else:
                cursor.execute("DELETE FROM `WarnsDB` WHERE `id`=%s AND `gid`=%s", (id, ctx.guild.id))
                embed = discord.Embed (
                    description=f"Предупреждение **{id}** было удалено", 
                    color = 0xe871ff
                )
                embed.add_field(name='Модератор', value=ctx.author.mention)
                await ctx.send (embed=embed)
                
        self.con.commit()

    @commands.command(
        usage="resetwarns  [пользователь]",
        description="Снять все предупреждение пользователю",
        brief="resetwarns @Miracle"
        )
    @commands.has_any_role(roles_config.discord_roles['admin'])
    async def resetwarns(self, ctx, user: discord.Member):
        with self.con.cursor() as cursor:
            cursor.execute("SELECT gid, uid FROM `WarnsDB` WHERE `gid`=%s AND `id`=%s", (ctx.guild.id, id))
            if cursor.fetchone() == None:
                embed = discord.Embed (
                    description=f"Данного ID нету в базе!", 
                    color = ctx.author.color
                )
                await ctx.send (embed=embed)
            else:
                cursor.execute("DELETE FROM `WarnsDB` WHERE `uid`=%s AND `gid`=%s", (user.id, ctx.guild.id))
                embed = discord.Embed (
                    description=f"Предупреждения у **{user.mention}** былы удалены", 
                    color = 0xe871ff
                )
                embed.add_field(name='Модератор', value=ctx.author.mention)
                await ctx.send(embed=embed)
        self.con.commit()

    @commands.command()
    async def warns(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        else:
            pass
        embed = discord.Embed (
            description = f"Предупреждения участника {user} ({user.id})",
            color = 0xe871ff
            )

        with self.con.cursor() as cursor:
            cursor.execute("SELECT gid, uid FROM `WarnsDB` WHERE `gid`=%s AND `uid`=%s", (ctx.guild.id, user.id))
            if cursor.fetchone() == None:
                embed.add_field (
                    name=f"Предупреждений не найдено", 
                    value=f"** **", inline = False
                    )
        self.con.commit()

        with self.con.cursor() as cursor:
            cursor.execute("SELECT * FROM `WarnsDB` WHERE `gid`=%s AND `uid`=%s", (ctx.guild.id, user.id))
            rows = cursor.fetchall()
            for row in rows:
                embed.add_field (
                    name=f"ID: `{row[0]}` | Модератор: {row[4]}", 
                    value=f"*Причина:* {row[3]} - {row[5]}", 
                    inline = False
                    )
        self.con.commit()
        await ctx.send (embed=embed)

    @commands.command(
        usage="mute [пользователь] [время] (причина)",
        description="Можно заглушить пользователя на время",
        brief="mute @M1racle 10m Оскорбление\nmute @M1racle 10h Нарушение правил\nmute @M1racle 1d Он сам захотел"
        )
    @commands.has_any_role(roles_config.discord_roles['admin'])
    async def mute(self, ctx, user: discord.Member, duration, *, reason = "Причина не указана"):
        with self.con.cursor() as cursor:
            if user == ctx.author:
                embed = discord.Embed ( 
                    description=f"Ты не можешь заглушить самого себя!", 
                    color = 0xfa4c4d
                    )
                await ctx.send (embed=embed)
            elif user == ctx.guild.owner:
                embed = discord.Embed (
                    description=f"Ты не можешь заглушить владельца сервера!", 
                    color = 0xfa4c4d
                    )
                await ctx.send (embed=embed)
            elif ctx.author.top_role.position < user.top_role.position:
                embed = discord.Embed (
                    description=f"Ты не можешь заглушить человека с ролью выше твоей!", 
                    color = 0xfa4c4d
                    )
                await ctx.send (embed=embed)
            else:
                role = ctx.guild.get_role(CONFIG['m_role_id'])
                time = None
                type = None
                if duration.endswith("s"):
                    duration, type = re.findall(r'(\d+)([a-zA-Z])', duration)[0]
                    time = duration
                    type = "сек."
                elif duration.endswith("m"):
                    duration, type = re.findall(r'(\d+)([a-zA-Z])', duration)[0]
                    time = int(duration)*60
                    type = "мин."
                elif duration.endswith("h"):
                    duration, type = re.findall(r'(\d+)([a-zA-Z])', duration)[0]
                    time = int(duration)*60*60
                    type = "ч."
                elif duration.endswith("d"):
                    duration, type = re.findall(r'(\d+)([a-zA-Z])', duration)[0]
                    time = int(duration)*60*60*24
                    type = "дн."
                else:
                    await ctx.send(content="Неправильный формат времени", delete_after=5)

                await user.add_roles(role)
                embed=discord.Embed(title=f"✅ | Участник {user.name} замьючен! 🙊", color=0xe871ff)
                embed.add_field(name="Модератор", value=ctx.author.mention, inline=True)
                embed.add_field(name="Срок", value=f"{duration} {type}", inline=True)
                if reason != "Причина не указана":
                    embed.add_field(name="Причина", value=reason, inline=True)
                await ctx.send(embed=embed)
                timestamp = datetime.now().timestamp() + int(time)
                cursor.execute(f"INSERT INTO `MutesDB` VALUES (NULL, '{ctx.guild.id}', '{user.id}', '{reason}', '{timestamp}')")
        self.con.commit()

    @commands.command(
        usage="unmute [пользователь]",
        description="Можно размутить пользователя",
        brief="unmute @M1racle"
        )
    @commands.has_any_role(roles_config.discord_roles['admin'])
    async def unmute(self, ctx, user: discord.Member):
        if user == ctx.author:
            embed = discord.Embed ( 
                description=f"Ты не можешь размутить самого себя!", 
                color = 0xfa4c4d
                )
            await ctx.send(embed=embed)
        elif ctx.author.top_role.position < user.top_role.position:
            embed = discord.Embed (
                description=f"Ты не можешь размутить человека с ролью выше твоей!", 
                color = 0xfa4c4d
                )
            await ctx.send(embed=embed)
        else:
            with self.con.cursor() as cursor:
                role = ctx.guild.get_role(CONFIG['m_role_id'])
                cursor.execute(f"DELETE FROM MutesDB WHERE uid='{user.id}'")
            await user.remove_roles(role)
            embed = discord.Embed (
                    description=f"Размут", 
                    color = 0xe871ff
                    )
            embed.add_field(name="Модератор",value=ctx.author.mention)
            embed.add_field(name="Участник",value=user)
            await ctx.send(embed=embed)

    @commands.command(
        usage="kick [пользователь] (причина)",
        description="Можно кикнуть пользователя",
        brief="kick @M1racle Оскорбление\kick @M1racle"
        )
    @commands.has_any_role(roles_config.discord_roles['admin'])
    async def kick(self, ctx, user: discord.Member, *, reason = "Причина не указана"):
        if user == ctx.author:
            embed = discord.Embed ( 
                description=f"Ты не можешь кикнуть самого себя!", 
                color = 0xfa4c4d
                )
            await ctx.send(embed=embed)
        elif user == ctx.guild.owner:
            embed = discord.Embed (
                description=f"Ты не можешь кикнуть владельца сервера!", 
                color = 0xfa4c4d
                )
            await ctx.send(embed=embed)
        elif ctx.author.top_role.position < user.top_role.position:
            embed = discord.Embed (
                description=f"Ты не можешь кикнуть человека с ролью выше твоей!", 
                color = 0xfa4c4d
                )
            await ctx.send (embed=embed)
        else:
            await user.kick(reason=reason)
            embed = discord.Embed (
                    description=f"Кик с сервера", 
                    color = 0xe871ff
                    )
            embed.add_field(name="Модератор",value=ctx.author.mention)
            embed.add_field(name="Участник",value=user)
            await ctx.send(embed=embed)

    @commands.command(
        usage="ban [пользователь] (причина)",
        description="Можно забанить пользователя",
        brief="ban @M1racle Оскорбление\ban @M1racle"
        )
    @commands.has_any_role(roles_config.discord_roles['admin'])
    async def ban(self, ctx, user: discord.Member, *, reason = "Причина не указана"):
        if user == ctx.author:
            embed = discord.Embed ( 
                description=f"Ты не можешь забанить самого себя!", 
                color = 0xfa4c4d
                )
            await ctx.send(embed=embed)
        elif user == ctx.guild.owner:
            embed = discord.Embed (
                description=f"Ты не можешь забанить владельца сервера!", 
                color = 0xfa4c4d
                )
            await ctx.send(embed=embed)
        elif ctx.author.top_role.position < user.top_role.position:
            embed = discord.Embed (
                description=f"Ты не можешь забанить человека с ролью выше твоей!", 
                color = 0xfa4c4d
                )
            await ctx.send (embed=embed)
        else:
            await user.ban(reason=reason)
            embed = discord.Embed (
                    description=f"Бан", 
                    color = 0xe871ff
                    )
            embed.add_field(name="Модератор",value=ctx.author.mention)
            embed.add_field(name="Участник",value=user)
            await ctx.send(embed=embed)

    @commands.command(
        usage="unban [пользователь]",
        description="Можно разбанить пользователя",
        brief="unban 271002810622017536"
        )
    @commands.has_any_role(roles_config.discord_roles['admin'])
    async def unban(self, ctx, user_id: int):
        user = await self.bot.fetch_user(user_id)
        banned_users = await ctx.guild.bans()
        for ban_entry in banned_users:
            ban_user = ban_entry.user
            if user == ban_user:
                await ctx.guild.unban(user)
                embed = discord.Embed (
                    description=f"Разбан", 
                    color = 0xe871ff
                    )
                embed.add_field(name="Модератор",value=ctx.author.mention)
                embed.add_field(name="ID Участник",value=user)
                await ctx.send(embed=embed)
                return
        embed = discord.Embed (
            description=f"***{user}*** не забанен на данном сервере", 
            color = 0xfa4c4d
            )
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Moderation(bot))