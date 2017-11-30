import sqlite3

conn = sqlite3.connect('tugas2.db')

conn.execute('''CREATE TABLE ping
         (user_id VARCHAR PRIMARY KEY     NOT NULL,
         last_timestamp            DATETIME     NOT NULL);''')

conn.commit()
conn.close()
