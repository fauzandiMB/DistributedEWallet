import sqlite3

conn = sqlite3.connect('tugas2.db')

cursor = conn.execute('SELECT * FROM ping')

for row in cursor:
   print "user_id = ", row[0]
   print "last_timestamp = ", row[1]

conn.close()
