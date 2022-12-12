import sqlite3


conn = sqlite3.connect("database.db")
print("success")

conn.execute(
    """
    create table dests (name text, phone_number text, dest text, method text, time SMALLDATETIME)
    """
)
conn.execute(
    """create table images (image_name text, image_dir text, time SMALLDATETIME);"""
)
print("create table success")

conn.close()