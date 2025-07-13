import sqlite3
from core.brain.memory import DB_PATH

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Fetch last 5 interactions
cursor.execute("SELECT * FROM interactions ORDER BY id DESC LIMIT 5")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
