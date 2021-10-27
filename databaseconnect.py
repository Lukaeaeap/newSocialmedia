import sqlite3

# Probeer te verbinden met de database, print anders een error.
try:
    conn = sqlite3.connect("goodData.db")
    print("Opened database successfully")
except Exception as e:
    print("Error during connection: ", str(e))

conn.close
