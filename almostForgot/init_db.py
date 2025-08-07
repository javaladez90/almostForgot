import sqlite3


conn = sqlite3.connect("/data/tasks.db")
cursor = conn.cursor()


cursor.execute("""
               CREATE TABLE IF NOT EXISTS tasks (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   recipient TEXT NOT NULL,
                   message TEXT NOT NULL,
                   send_time TEXT NOT NULL
               )
               """)

conn.commit()
conn.close()