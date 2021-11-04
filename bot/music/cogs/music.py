import asyncio
import math
import re
from dataclasses import dataclass

import nextcord as discord
from nextcord.ext.commands.context import P
import lavalink
from nextcord.ext import commands, tasks
from nextcord.types.components import ButtonStyle
from nextcord.ui import view
from nextcord.webhook import async_
import pymysql
from configs.bd_config import CONFIG
url_rx = re.compile(r'https?://(?:www\.)?.+')


class LavalinkVoiceClient(discord.VoiceClient):

    def __init__(self, client: discord.Client, channel: discord.abc.Connectable):
        self.client = client
        self.channel = channel

        self.volume = 50
        
        # ensure there exists a client already
        if hasattr(self.client, 'lavalink'):
            self.lavalink = self.client.lavalink
        else:
            self.client.lavalink = lavalink.Client(client.user.id)
            self.client.lavalink.add_node(
                    '127.0.0.1',
                    2333,
                    'pass',
                    'us',
                    f'node-bot-{self.id}')
            self.lavalink = self.client.lavalink
        
    async def on_voice_server_update(self, data):
        # the data needs to be transformed before being handed down to
        # voice_update_handler
        lavalink_data = {
                't': 'VOICE_SERVER_UPDATE',
                'd': data
                }
        await self.lavalink.voice_update_handler(lavalink_data)

    async def on_voice_state_update(self, data):
        # the data needs to be transformed before being handed down to
        # voice_update_handler
        lavalink_data = {
                't': 'VOICE_STATE_UPDATE',
                'd': data
                }
        await self.lavalink.voice_update_handler(lavalink_data)

    async def connect(self, *, timeout: float, reconnect: bool) -> None:
        """
        Connect the client to the voice channel and create a player_manager
        if it doesn't exist yet.
        """
        # ensure there is a player_manager when creating a new voice_client
        self.lavalink.player_manager.create(guild_id=self.channel.guild.id)
        await self.channel.guild.change_voice_state(channel=self.channel)

    async def disconnect(self, *, force: bool) -> None:
        """
        Handles the disconnect.
        Cleans up running player and leaves the voice client.
        """
        player = self.lavalink.player_manager.get(self.channel.guild.id)

        # no need to disconnect if we are not connected
        if not force and not player.is_connected:
            return

        # None means disconnect
        await self.channel.guild.change_voice_state(channel=None)

        # update the channel_id of the player to None
        # this must be done because the on_voice_state_update that
        # would set channel_id to None doesn't get dispatched after the 
        # disconnect
        player.channel_id = None
        self.cleanup()

class MusicTime:
    
    def __init__(self, millis) -> None:
        seconds=(millis/1000)%60
        self.seconds = int(seconds)
        minutes=(millis/(1000*60))%60
        self.minutes = int(minutes)
        hours=(millis/(1000*60*60))%24
        self.hours = int(hours)

    def __str__(self) -> str:
        if self.hours > 0:
            return f'{self.hours:0>2.0f}:{self.minutes:0>2.0f}:{self.seconds:0>2.0f}'
        else:
            return f'{self.minutes:0>2.0f}:{self.seconds:0>2.0f}'

# MUSIC CLASS

class Music(commands.Cog):
    def __init__(self, client, id):
        self.client = client
        self.id = id
        self.controllers = {}
        self.con = pymysql.connect(
            host=CONFIG['host'],
            user=CONFIG['user'],
            password=CONFIG['password'],
            database=CONFIG['db'])
        if not hasattr(self.client, 'lavalink'):  # This ensures the client isn't overwritten during cog reloads.
            client.lavalink = lavalink.Client(client.user.id)
            client.lavalink.add_node('127.0.0.1', 2333, 'pass', 'eu', f'node-bot-{self.id}')  # Host, Port, Password, Region, Name

        lavalink.add_event_hook(self.track_hook)


    def cog_unload(self):
        """ Cog unload handler. This removes any event hooks that were registered. """
        self.client.lavalink._event_hooks.clear()

    async def cog_before_invoke(self, ctx):
        """ Command before-invoke handler. """
        guild_check = ctx.guild is not None
        #  This is essentially the same as `@commands.guild_only()`
        #  except it saves us repeating ourselves (and also a few lines).

        if guild_check:
            await self.ensure_voice(ctx)
            #  Ensure that the client and command author share a mutual voicechannel.

        return guild_check

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(error.original)
            # The above handles errors thrown in this cog and shows them to the user.
            # This shouldn't be a problem as the only errors thrown in this cog are from `ensure_voice`
            # which contain a reason string, such as "Join a voicechannel" etc. You can modify the above
            # if you want to do things differently.

    async def ensure_voice(self, ctx):
        """ This check ensures that the client and command author are in the same voicechannel. """
        player = self.client.lavalink.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
        # Create returns a player if one exists, otherwise creates.
        # This line is important because it ensures that a player always exists for a guild.

        # Most people might consider this a waste of resources for guilds that aren't playing, but this is
        # the easiest and simplest way of ensuring players are created.

        # These are commands that require the client to join a voicechannel (i.e. initiating playback).
        # Commands such as volume/skip etc don't require the client to be in a voicechannel so don't need listing here.
        print(ctx.command.name)
        should_connect = ctx.command.name in ('play','start',)

        if not ctx.author.voice or not ctx.author.voice.channel:
            # Our cog_command_error handler catches this and sends it to the voicechannel.
            # Exceptions allow us to "short-circuit" command invocation via checks so the
            # execution state of the command goes no further.
            raise commands.CommandInvokeError('Join a voicechannel first.')

        if not player.is_connected:
            if not should_connect:
                raise commands.CommandInvokeError('Not connected.')

            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            if not permissions.connect or not permissions.speak:  # Check user limit too?
                raise commands.CommandInvokeError('I need the `CONNECT` and `SPEAK` permissions.')

            player.store('channel', ctx.channel.id)
            await ctx.author.voice.channel.connect(cls=LavalinkVoiceClient)
        else:
            if int(player.channel_id) != ctx.author.voice.channel.id:
                raise commands.CommandInvokeError('You need to be in my voicechannel.')

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            # When this track_hook receives a "QueueEndEvent" from lavalink.py
            # it indicates that there are no tracks left in the player's queue.
            # To save on resources, we can tell the client to disconnect from the voicechannel.
            guild_id = int(event.player.guild_id)
            guild = self.client.get_guild(guild_id)
            await guild.voice_client.disconnect(force=True)

    @commands.command()
    async def start(self,ctx):
        self.musicloop.start()

    @commands.command(aliases=['p'])
    async def play(self, ctx, *, query: str):
        player = self.client.lavalink.player_manager.get(ctx.guild.id)
        query = query.strip('<>')

        if not url_rx.match(query):
            query = f'ytsearch:{query}'

        results = await player.node.get_tracks(query)

        if not results or not results['tracks']:
            return await ctx.send('Nothing found!')

        embed = discord.Embed(color=discord.Color.blurple())

        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']

            for track in tracks:
                player.add(requester=ctx.author.id, track=track)

            embed.title = 'Playlist Enqueued!'
            embed.description = f'{results["playlistInfo"]["name"]} - {len(tracks)} tracks'
        else:
            track = results['tracks'][0]
            embed.title = 'Track Enqueued'
            embed.description = f'[{track["info"]["title"]}]({track["info"]["uri"]})'

            track = lavalink.models.AudioTrack(track, ctx.author.id, recommended=True)
            player.add(requester=ctx.author.id, track=track)

        #await ctx.send(embed=embed)

        if not player.is_playing:
            await player.play()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        voice_state = member.guild.voice_client
        if member.id == self.client.user.id:
            if after.channel is None:
                with self.con.cursor() as cursor:

                    cursor.execute(f"UPDATE `MusicDB` SET `channel`='' WHERE `id`={self.id}")
                    self.con.commit()

        if voice_state is None:
            return 

        if len(voice_state.channel.members) == 1:
            await voice_state.disconnect(cls=LavalinkVoiceClient)


    @commands.command()
    async def pause(self, ctx):
        player = self.client.lavalink.player_manager.get(ctx.guild.id)
        if player.paused:
            await ctx.send('Музыка уже стоит на паузе.')
            return
        await ctx.send('Данное произведение поставлено на паузу.')
        await player.set_pause(True)

    @commands.command()
    async def skip(self, ctx):
        player = self.client.lavalink.player_manager.get(ctx.guild.id)
        await player.skip()

    @commands.command()
    async def shuffle(self, ctx):
        player = self.client.lavalink.player_manager.get(ctx.guild.id)
        shuffle = player.shuffle
        if shuffle:
            await ctx.send('Музыка не будет перемешиваться')
            player.set_shuffle(False)
        else:
            await ctx.send('Музыка перемешана')
            player.set_shuffle(True)

    @commands.command()
    async def loop(self, ctx):
        player = self.client.lavalink.player_manager.get(ctx.guild.id)
        repeat = player.repeat
        if repeat:
            await ctx.send('Музыка не зацыклена')
            player.set_repeat(False)
        else:
            await ctx.send('Музыка зацыклена')
            player.set_repeat(True)

    @commands.command()
    async def resume(self, ctx):
        player = self.client.lavalink.player_manager.get(ctx.guild.id)

        if not player.paused:
            await ctx.send('Музыка уже играет.')
            return

        await player.set_pause(False) 

        
    @commands.command()
    async def queue(self, ctx):
        player = self.client.lavalink.player_manager.get(ctx.guild.id)
        current = player.current
        queue_text = ''

        requester = ctx.guild.get_member(current.requester)
        current_time = self.MusicTime(current.duration)
        current_pos = self.MusicTime(player.position)

        embed=discord.Embed(title="Очередь", description=f"Сейчас: [{current.title}]({current.uri}) ({current_pos}/{current_time}) — {requester.mention}")
        if player.queue:
            for i,track in enumerate(player.queue):
                duration = self.MusicTime(track.duration)
                requester = ctx.guild.get_member(track.requester)
                queue_text += f'**{i+1} > ** [{track.title}]({track.uri}) ({duration}) — {requester.mention}\n'
        else:
            queue_text = '**Очередь пустая**'
        embed.add_field(name='\u200b', value=queue_text, inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    async def now(self, ctx):
        player = self.client.lavalink.player_manager.get(ctx.guild.id)

        if not player.current:
            return await ctx.send('В данный момент ничего не воспроизводиться.')

        controller = self.get_controller(ctx)
        await controller.now_playing.delete()
        embed = discord.Embed (title="В данный момент играет", description=f"[{player.current}]({player.current.uri})", color=ctx.author.color)

        controller.now_playing = await ctx.send(embed=embed)    



    @commands.command(aliases=['dc', 'stop'])
    async def disconnect(self, ctx):
        """ Disconnects the player from the voice channel and clears its queue. """
        player = self.client.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            # We can't disconnect, if we're not connected.
            return await ctx.send('Not connected.')

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            # Abuse prevention. Users not in voice channels, or not in the same voice channel as the client
            # may not disconnect the client.
            return await ctx.send('You\'re not in my voicechannel!')

        # Clear the queue to ensure old tracks don't start playing
        # when someone else queues something.
        player.queue.clear()
        # Stop the current track so Lavalink consumes less resources.
        await player.stop()
        # Disconnect from the voice channel.
        await ctx.voice_client.disconnect(force=True)
        await ctx.send('*⃣ | Disconnected.')

    @tasks.loop(seconds=1)
    async def musicloop(self):
        with self.con.cursor() as cursor:
            cursor.execute(f"SELECT `channel`,`add_to_queue`,`queue_author` FROM `MusicDB` WHERE `id`={self.id}")
            data = cursor.fetchone()
            player = self.client.lavalink.player_manager.get(398857722159824907)
            if data[1] != '':
                if not self.client.voice_clients is None:
                    if not player.is_connected:
                        player.store('channel', int(data[0]))
                        await self.client.get_channel(int(data[0])).connect(cls=LavalinkVoiceClient)
                    authors = data[2].split(',')
                    querry_list = data[1].split(',')
                    authors.pop()
                    querry_list.pop()
                    print(f'QUERRY: {querry_list}')
                    for i, query in enumerate(querry_list):
                        print(f'BOT-{self.id}: {query}')
                        author = int(authors[i])
                        query = query.strip('<>')

                        if not url_rx.match(query):
                            query = f'ytsearch:{query}'

                        results = await player.node.get_tracks(query)

                        embed = discord.Embed(color=discord.Color.blurple())

                        if results['loadType'] == 'PLAYLIST_LOADED':
                            tracks = results['tracks']

                            for track in tracks:
                                player.add(requester=author, track=track)

                            embed.title = 'Playlist Enqueued!'
                            embed.description = f'{results["playlistInfo"]["name"]} - {len(tracks)} tracks'
                        else:
                            track = results['tracks'][0]
                            embed.title = 'Track Enqueued'
                            embed.description = f'[{track["info"]["title"]}]({track["info"]["uri"]})'

                            track = lavalink.models.AudioTrack(track, author, recommended=True)
                            player.add(requester=author, track=track)

                        #await ctx.send(embed=embed)

                        if not player.is_playing:
                            await player.play()
                    cursor.execute(f"UPDATE `MusicDB` SET `add_to_queue`='',`queue_author`='' WHERE `id`={self.id}")
                    self.con.commit()


    @commands.command()
    async def mmenu(self, ctx):

        class Menu(discord.ui.View):

            def __init__(self, client, ctx, *, timeout=None):
                super().__init__(timeout=timeout)
                self.client = client
                self.ctx = ctx
                self.controller = Music(self.client)
                self.queue_pos = 0
                self.message = None

            async def send_embed(self):
                player = self.controller.client.lavalink.player_manager.get(self.ctx.guild.id)
                queue_text = ''
                
                if player.current:
                    current = player.current
                    requester = self.ctx.guild.get_member(current.requester)
                    current_time = MusicTime(current.duration)
                    current_pos = MusicTime(player.position)
                    current_text = f"Сейчас: [{current.title}]({current.uri}) ({current_pos}/{current_time}) — {requester.mention}"
                else:
                    current_text = 'Сейчас ничего не играет'

                self.embed=discord.Embed(title="Меню музыки", color=0xE100FF, description=current_text)
                if player.queue:
                    queue = player.queue[0+(5*self.queue_pos):5*(self.queue_pos+1)]
                    for i,track in enumerate(queue):
                        duration = MusicTime(track.duration)
                        requester = self.ctx.guild.get_member(track.requester)
                        queue_text += f'**{i+1} > ** [{track.title}]({track.uri}) ({duration}) — {requester.mention}\n'
                else:
                    queue_text = '**Очередь пустая**'
                self.embed.add_field(name='Очередь', value=queue_text, inline=True)
                self.message = await self.ctx.send(embed=self.embed, view=self)

            async def update_embed(self):
                player = self.client.lavalink.player_manager.get(self.ctx.guild.id)
                queue_text = ''
                if player.current:
                    current = player.current
                    requester = self.ctx.guild.get_member(current.requester)
                    current_time = MusicTime(current.duration)
                    current_pos = MusicTime(player.position)
                    current_text = f"Сейчас: [{current.title}]({current.uri}) ({current_pos}/{current_time}) — {requester.mention}"
                else:
                    current_text = 'Сейчас ничего не играет'

                self.embed=discord.Embed(title="Меню музыки", color=0xE100FF, description=current_text)
                if player.queue:
                    queue = player.queue[0+(5*self.queue_pos):5*(self.queue_pos+1)]
                    for i,track in enumerate(queue):
                        duration = MusicTime(track.duration)
                        requester = self.ctx.guild.get_member(track.requester)
                        queue_text += f'**{i+1+(5*self.queue_pos)} > ** [{track.title}]({track.uri}) ({duration}) — {requester.mention}\n'
                else:
                    queue_text = '**Очередь пустая**'
                self.embed.add_field(name='Очередь', value=queue_text, inline=True)
                await self.message.edit(embed=self.embed, view = self)


            @discord.ui.button(emoji='⏪', row=0, disabled=True)
            async def prev_queue(self, button, interaction):
                player = self.controller.client.lavalink.player_manager.get(self.ctx.guild.id)
                
                self.queue_pos -= 1

                if self.queue_pos == 0:
                    self.children[0].disabled = True

                if self.queue_pos < math.ceil(len(player.queue)/5)-1:
                    self.children[2].disabled = False
                await self.update_embed()


            @discord.ui.button(emoji='⏸️', row=0)
            async def pause(self, button, interaction):
                player = self.client.lavalink.player_manager.get(self.ctx.guild.id)
                
                if not player.paused:
                    await player.set_pause(True)
                    self.children[1].emoji = '▶️'
                else:
                    await player.set_pause(False)
                    self.children[1].emoji = '⏸️'

                await self.update_embed()
            
            @discord.ui.button(emoji='⏩', row=0)
            async def next_queue(self, button, interaction):
                player = self.controller.client.lavalink.player_manager.get(self.ctx.guild.id)
                
                if self.queue_pos == 0:
                    self.children[0].disabled = False
                print(math.ceil(len(player.queue)/5))
                
                self.queue_pos += 1
                if self.queue_pos == math.ceil(len(player.queue)/5)-1:
                    self.children[2].disabled = True

                await self.update_embed()

            
            @discord.ui.button(emoji='⏭️', row=1)
            async def skip(self, button, interaction):
                player = self.controller.client.lavalink.player_manager.get(self.ctx.guild.id)
                await player.skip()

                await self.update_embed()
            
            @discord.ui.button(label='\u200b', row=1, disabled=True)
            async def f1(self, button, interaction):
                print('prev')

            @discord.ui.button(emoji='⏹️', row=1)
            async def stop(self, button, interaction):
                player = self.controller.client.lavalink.player_manager.get(self.ctx.guild.id)

                player.queue = []
                await player.play()

                await self.update_embed()

            @discord.ui.button(emoji='🔀', style=discord.ButtonStyle.red, row=2)
            async def mix(self, button, interaction):
                player = self.controller.client.lavalink.player_manager.get(self.ctx.guild.id)

                if player.shuffle:
                    self.children[6].style = discord.ButtonStyle.red
                    player.set_shuffle(False)
                else:
                    self.children[6].style = discord.ButtonStyle.green
                    player.set_shuffle(True)

                await self.update_embed()

            @discord.ui.button(label='\u200b', row=2, disabled=True)
            async def f2(self, button, interaction):
                print('prev')
            
            @discord.ui.button(emoji='🔁', style=discord.ButtonStyle.red, row=2)
            async def loop(self, button, interaction):
                player = self.controller.client.lavalink.player_manager.get(self.ctx.guild.id)

                if player.repeat:
                    self.children[8].style = discord.ButtonStyle.red
                    player.set_repeat(False)
                else:
                    self.children[8].style = discord.ButtonStyle.green
                    player.set_repeat(True)

                await self.update_embed()

        menu = Menu(self.client, ctx)

        if menu.message is None:
            await menu.send_embed()
        else:
            await menu.update_embed()
        

def setup(client, id):
    client.add_cog(Music(client, id))