import sqlite3 as sql

from flask import Flask, render_template, request

app = Flask(__name__)


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
            result_1 = request.form["dest_1"]
            result_2 = request.form["dest_2"]

            with sql.connect("database.db") as con:

                cur = con.cursor()
                cur.execute(
                    "INSERT INTO dests (dest, temp) VALUES (?,?)",
                    (result_1, result_2),
                )
            msg = "Success"
            con.close()

        except:
            con.rollback()
            msg = "error"
        finally:
            return render_template("result.html", msg=msg)


@app.route("/dest_result")
def dest_result():
    con = sql.connect("database.db")  # database.db파일에 접근.
    cur = con.cursor()
    cur.execute("select dest from dests limit 1")

    rows = cur.fetchall()
    result = str(rows[0][0])

    con.close()
    return render_template("dest_result.html", result=result)


if __name__ == "__main__":
    app.debug = True
    app.run()
