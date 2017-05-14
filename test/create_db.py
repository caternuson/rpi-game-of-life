import sqlite3

FILENAME = 'life_stats.db'
SQL = '''CREATE TABLE STATS (ID BLOB PRIMARY KEY,
                             GENERATIONS INT,
                             PERIOD INT);'''

conn = sqlite3.connect(FILENAME)
conn.execute(SQL)
conn.close()