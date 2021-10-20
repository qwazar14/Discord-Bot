import sqlite3

conn = sqlite3.connect("users.db")  # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()

# Создание таблицы
cursor.execute("""CREATE TABLE stamps
                  ( user_id text,
                    stamp_id text,
                    score text                   
                    )
               """)
