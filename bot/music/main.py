import pymysql
import sys,os
import signal
import subprocess
from time import sleep

from configs.bd_config import CONFIG

con = pymysql.connect(
            host=CONFIG['host'],
            user=CONFIG['user'],
            password=CONFIG['password'],
            database=CONFIG['db']) 
    
cursor = con.cursor()
cursor.execute('SELECT `id`,`token` FROM `MusicDB`')
data = cursor.fetchall()
bots = []

for bot in data:
    bots.append(subprocess.Popen(f'python music/bot.py "{bot[0]}" "{bot[1]}"'))
    sleep(1)
    
def kill_child():
    for bot in bots:
        os.kill(bot.pid, signal.SIGTERM)

import atexit
atexit.register(kill_child)

while True:
    sleep(1)

