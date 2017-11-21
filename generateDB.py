import sqlite3

conn = sqlite3.connect('ewallet.db')

conn.execute('''CREATE TABLE account
         (user_id VARCHAR PRIMARY KEY     NOT NULL,
         nama           VARCHAR    NOT NULL,
         saldo            INT     NOT NULL);''')

conn.execute('''INSERT INTO account (user_id, nama, saldo) VALUES("1406623266", "Fauzandi Muhammad Baskara", '1000000000');''')

conn.commit()

conn.close()
