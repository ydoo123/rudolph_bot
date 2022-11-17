import sqlite3


conn = sqlite3.connect("database.db")
print("create db success")

conn.execute(
    """
    CREATE TABLE dests (name text, phone_number text, dest text, method text);
    """
)
print("create table success")

conn.close()
