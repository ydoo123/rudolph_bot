import sqlite3 as sql
import json
import datetime
import os
from werkzeug.utils import secure_filename

from flask import Flask, render_template, request

app = Flask(__name__)
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
dest_list = [str(i) for i in range(101, 132)]
dest_list.append("128-1")


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/user_form")
def new_user():
    print("user_form")
    return render_template("user.html")


@app.route("/user_info", methods=["POST", "GET"])
def user_info():
    if request.method == "POST":
        try:
            user_email = request.form["user_email"]
            user_password = request.form["user_password"]

            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO users (email, password) VALUES (?,?)",
                    (user_email, user_password),
                )
            msg = "Success"
            con.close()

        except:
            con.rollback()
            msg = "error"
        finally:
            return render_template("result.html", msg=msg)


@app.route("/list")
def list():
    con = sql.connect("database.db")  # database.db파일에 접근.
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from users")

    rows = cur.fetchall()
    return render_template("list.html", rows=rows)


@app.route("/dest_form")
def new_dest():
    print("dest_form")
    return render_template("dest_form.html")


@app.route("/dest_info", methods=["POST", "GET"])
def dest_info():
    if request.method == "POST":
        try:
            name = request.form["name"]  # 이름
            phone_number = request.form["phone_number"]  # 전화번호
            dest = request.form["dest"]  # 목적지
            method = request.form.get("method")  # 수령방법

            time_now = datetime.datetime.now()
            time_val = time_now.strftime(TIME_FORMAT)

            with sql.connect("database.db") as con:

                cur = con.cursor()
                cur.execute(
                    "INSERT INTO dests (name, phone_number, dest, method, time) VALUES (?,?,?,?,?)",
                    (name, phone_number, dest, method, time_val),
                )
            msg = "Success"
            con.close()

        except:
            con.rollback()
            msg = "error"
            return render_template("result.html", msg=msg)

        finally:
            return render_template("form_result.html")


@app.route("/dest_result")
def dest_result():
    con = sql.connect("database.db")  # database.db파일에 접근.
    cur = con.cursor()
    cur.execute("select dest, method from dests limit 1")

    rows = cur.fetchall()
    dest = str(rows[0][0])
    method = str(rows[0][1])

    con.close()
    return render_template("dest_result.html", dest=dest, method=method)


@app.route("/get_dest")
def get_dest():  # access to get dest json
    con = sql.connect("database.db")  # database.db파일에 접근.
    cur = con.cursor()
    cur.execute("select dest, method from dests order by time desc limit 1")

    rows = cur.fetchall()
    dest = str(rows[0][0])
    method = str(rows[0][1])

    con.close()
    result_dict = {"dest": dest, "method": method}
    result_json = json.dumps(result_dict)

    return result_json


@app.route("/fileUpload", methods=["GET", "POST"])
def file_upload():
    try:
        if request.method == "POST":
            time_now = datetime.datetime.now()
            time_val = time_now.strftime(TIME_FORMAT)

            file = request.files["file"]
            file.save("static/uploads/" + secure_filename(file.filename))
            # files = os.listdir("static/uploads")

            con = sql.connect("database.db")
            cursor = con.cursor()
            # 파일명과 파일경로를 데이터베이스에 저장함
            cursor.execute(
                "INSERT INTO images (image_name, image_dir, time) VALUES (?, ?, ?)",
                (
                    secure_filename(file.filename),
                    "static/uploads/" + secure_filename(file.filename),
                    time_val,
                ),
            )
            con.close()

            return "susccess"

    except:
        con.rollback()
        cursor.close()
        con.close()

        return "upload failed"


@app.route("/form_result")
def form_result():
    return render_template("form_result.html")


if __name__ == "__main__":
    app.debug = True
    app.run()
