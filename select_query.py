import sqlite3

conn = sqlite3.connect('ewallet.db')

cursor = conn.execute("SELECT * FROM account;")

for row in cursor:
   print "user_id = ", row[0]
   print "nama = ", row[1]
   print "saldo = ", row[2], "\n"

# conn.execute('UPDATE account SET saldo = 999974000 WHERE user_id 1406623266')
# conn.commit()
