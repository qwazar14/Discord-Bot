import sqlite3

conn = sqlite3.connect("user_stamps.db")  # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()

# Создание таблицы
cursor.execute("""CREATE TABLE stamps
                  ( user_id,
                    stamp_id,
                    stamp_counter                    
                    )
               """)
