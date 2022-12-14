import sqlite3 as sql
import json
import datetime

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from check_value import format_phone_number, check_dest, check_phone_number
import os

app = Flask(__name__)
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


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
            return render_template("error.html", msg=msg)


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


@app.route("/dest_form_test")
def new_dest_test():
    print("dest_form")
    return render_template("dest_form_test.html")


@app.route("/dest_info", methods=["POST", "GET"])
def dest_info():
    dest_list = [str(i) for i in range(113, 132)]

    if request.method == "POST":
        try:
            name = request.form["name"]  # 이름
            phone_number = request.form["phone_number"]  # 전화번호
            dest = request.form["dest"]  # 목적지
            method = request.form["method"]  # 수령방법

            time_now = datetime.datetime.now() + datetime.timedelta(hours=9)
            time_val = time_now.strftime(TIME_FORMAT)

            with sql.connect("database.db") as con:

                cur = con.cursor()
                cur.execute(
                    "INSERT INTO dests (name, phone_number, dest, method, time) VALUES (?,?,?,?,?)",
                    (name, phone_number, dest, method, time_val),
                )
            msg = "Success"
            con.close()

            return render_template(
                "form_result.html", map=f"static/images/maps/map_{dest}.png"
            )

        except:
            con.rollback()
            msg = "error"
            return render_template("error.html", msg=msg)


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
    cur.execute("select dest, method, time from dests order by time desc limit 1")

    rows = cur.fetchall()
    dest = str(rows[0][0])
    method = str(rows[0][1])
    time = str(rows[0][2])

    con.close()
    result_dict = {"dest": dest, "method": method, "time": time}
    result_json = json.dumps(result_dict)

    return result_json


@app.route("/status")
def status():
    con = sql.connect("database.db")  # database.db파일에 접근.
    cur = con.cursor()
    cur.execute("select dest, time from dests order by time desc limit 1")

    rows = cur.fetchall()
    dest = str(rows[0][0])
    time = str(rows[0][1])
    splited_time = time.split(" ")
    hour = splited_time[1].split(":")[0]
    minute = splited_time[1].split(":")[1]

    return render_template("status.html", dest=dest, hour=hour, minute=minute)


@app.route("/fileUpload", methods=["GET", "POST"])
def file_upload():
    if request.method == "POST":
        time_now = datetime.datetime.now() + datetime.timedelta(hours=9)
        time_val = time_now.strftime(TIME_FORMAT)

        f = request.files["file"]
        f.save("static/uploads/" + secure_filename(f.filename))
        files = os.listdir("static/uploads")

        con = sql.connect("database.db")
        cursor = con.cursor()
        # 파일명과 파일경로를 데이터베이스에 저장함
        cursor.execute(
            "INSERT INTO images (image_name, image_dir, time) VALUES (?, ?, ?)",
            (
                secure_filename(f.filename),
                "static/uploads/" + secure_filename(f.filename),
                time_val,
            ),
        )
        data = cursor.fetchall()

        if not data:
            con.commit()
            cursor.close()
            con.close()

            return "not data"

        else:
            con.rollback()
            cursor.close()
            con.close()

            return "upload failed"


@app.route("/status_main")
def status_main():
    con = sql.connect("database.db")  # database.db파일에 접근.

    cur_dest = con.cursor()
    cur_dest.execute("select dest, time from dests order by time desc limit 1")
    rows_dest = cur_dest.fetchall()

    dest = str(rows_dest[0][0])
    time_dest = str(rows_dest[0][1])

    cur_image = con.cursor()
    cur_image.execute(
        "select image_name, image_dir, time from images order by time desc limit 1"
    )
    rows_image = cur_image.fetchall()
    if not rows_image:
        return render_template(
            "status_loading.html", map=f"static/images/maps/map_{dest}.png"
        )
    image_name = str(rows_image[0][0])
    image_dir = str(rows_image[0][1])
    time_image = str(rows_image[0][2])

    if time_image > time_dest:
        return render_template(
            "status_main.html",
            image=image_dir,
            map=f"static/images/maps/map_{dest}.png",
        )

    else:
        return render_template(
            "status_loading.html", map=f"static/images/maps/map_{dest}.png"
        )

    return None


if __name__ == "__main__":
    app.debug = True
    app.run()
