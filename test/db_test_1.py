import sqlite3 as sql
import logging

from flask import Flask, render_template, request


con = sql.connect(
    "/home/ubuntu/test_server/rudolph_bot/database.db"
)  # database.db파일에 접근.
# con.row_factory = sql.Row

cur = con.cursor()
cur.execute("select dest from dests limit 1")

rows = cur.fetchall()
result = str(rows[0][0])

con.close()

print(rows)
