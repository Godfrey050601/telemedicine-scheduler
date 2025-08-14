from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "telemedicine_secret"

DB_NAME = "appointments.db"

# Create database table if it doesn't exist
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS appointments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    date TEXT NOT NULL,
                    time TEXT NOT NULL,
                    doctor TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        date = request.form["date"]
        time = request.form["time"]
        doctor = request.form["doctor"]

        if not name or not email or not date or not time or not doctor:
            flash("All fields are required!", "danger")
        else:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("INSERT INTO appointments (name, email, date, time, doctor) VALUES (?, ?, ?, ?, ?)",
                      (name, email, date, time, doctor))
            conn.commit()
            conn.close()
            flash("Appointment booked successfully!", "success")
            return redirect(url_for("index"))

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM appointments ORDER BY date, time")
    appointments = c.fetchall()
    conn.close()
    return render_template("index.html", appointments=appointments)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
