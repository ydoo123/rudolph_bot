import sqlite3


conn = sqlite3.connect("database.db")
print("create db success")

conn.execute(
    """
    create table images (image_name text, image_dir text, time SMALLDATETIME);
    """
)
print("create table success")

conn.close()
