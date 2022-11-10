import sqlite3


conn = sqlite3.connect('database.db')
print('create db success')

conn.execute(
    """
    create table users (email test, password text)
    """
)
print('create table success')

conn.close()