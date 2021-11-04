import nextcord as discord
import nextcord
import pymysql
from nextcord.ext import commands
from configs.channel_config import music_channel
from configs.bd_config import CONFIG

class MusicController(commands.Cog):

    def __init__(self, client) -> None:
        super().__init__()
        self.client = client
        self.con = pymysql.connect(
            host=CONFIG['host'],
            user=CONFIG['user'],
            password=CONFIG['password'],
            database=CONFIG['db']) 

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.voice is None:
                    #TODO: Make invisible message if user not in voice
                    return  

        with self.con.cursor() as cursor:
            cursor.execute(f"SELECT `menu_channel` FROM `MusicDB`")
            music_menu_channel = [i[0] for i in cursor.fetchall()]
            author_voice = message.author.voice.channel.id

            if str(message.channel.id) in music_menu_channel:
                print('MUSIC MENU')
                cursor.execute(f"SELECT * FROM `MusicDB` WHERE `channel`='{author_voice}'")
                res = cursor.fetchone()
                if res is not None:
                    print('MUSIC MENU UPDATE')
                    queue = res[5]
                    author_queue = res[6]
                    author_queue += f'{message.author.id},'
                    queue += f'{message.content},'
                    cursor.execute(f"UPDATE `MusicDB` SET `add_to_queue`='{queue}',`queue_author`='{author_queue}' WHERE `channel`='{author_voice}'")
                    self.con.commit()
                    return

            if message.channel.id == music_channel:
                print('MUSIC CHANNEL')
                cursor.execute(f"SELECT * FROM `MusicDB` WHERE `channel`='{author_voice}'")
                res = cursor.fetchone()  
                if res is not None:
                    queue = res[5]
                    author_queue = res[6]
                    author_queue += f'{message.author.id},'
                    queue += f'{message.content},'
                    cursor.execute(f"UPDATE `MusicDB` SET `add_to_queue`='{queue}',`queue_author`='{author_queue}' WHERE `channel`='{author_voice}'")
                    self.con.commit()
                    return
                
                cursor.execute("SELECT * FROM `MusicDB` WHERE `channel`=''")
                bot = cursor.fetchone()
                
                if bot is None:
                    #TODO: Make invisible message if no bots avaliable
                    return

                print('MUSIC CHANNEL UPDATE')
                queue = bot[5]
                author_queue = bot[6]
                author_queue += f'{message.author.id},'
                queue += f'{message.content},'
                cursor.execute(f"UPDATE `MusicDB` SET `channel`='{author_voice}',`add_to_queue`='{queue}',`queue_author`='{author_queue}' WHERE `id`='{bot[0]}'")
                self.con.commit()


def setup(client):
    client.add_cog(MusicController(client))