from flask import Flask, render_template, request
import sqlite3

web = Flask(__name__)


connect = sqlite3.connect("participants.db")
connect.execute("CREATE TABLE IF NOT EXISTS PARTICIPANTS (name TEXT, email TEXT, city TEXT, country TEXT, phone TEXT)")


@web.route("/")
@web.route("/home")
def index():
    return render_template("index.html")


@web.route("/join", methods=["POST", "GET"])
def join():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        city = request.form["city"]
        country = request.form["country"]
        phone = request.form["phone"]
        with sqlite3.connect("participants.db") as db:
            cursor = db.cursor()
            cursor.execute("INSERT INTO PARTICIPANTS (name, email, city, country, phone) VALUES (?, ?, ?, ?, ?)",
                           (name, email, city, country, phone))
            db.commit()
        return render_template("index.html")
    else:
        return render_template("join.html")


@web.route("/participants")
def participants():
    db = sqlite3.connect("participants.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM PARTICIPANTS")
    data = cursor.fetchall()
    return render_template("participants.html", data=data)


if __name__ == "__main__":
    web.run(debug=True)
