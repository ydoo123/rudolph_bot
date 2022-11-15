import sqlite3


conn = sqlite3.connect("database.db")
print("create db success")

conn.execute(
    """
    alter table dests add column temp [text];
    """
)
print("create table success")

conn.close()
