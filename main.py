from flask import Flask, render_template, request, redirect
import sqlite3 as sql
import threading
import time
import os
import db

app = Flask(__name__)

@app.route("/")
def home():
    mode = request.args.get("mode", "light")
    conn = sql.connect(db.db_filename)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM user")
    users = cursor.fetchall()
    conn.close()
    return render_template("home.html", mode=mode, users=users)

@app.route("/about")
def about():
    mode = request.args.get("mode", "light")
    return render_template("about.html", mode=mode)



@app.route("/d3adb33f")
def reset_database():
    try:
        conn = sql.connect(db.db_filename)
        db.reset_database(conn)
        conn.close()
        return redirect("/")
    except Exception as e:
        return f"An error occurred: {e}", 500

if __name__ == "__main__":
    conn = sql.connect(db.db_filename)
    db.db_init(conn)
    db.create_user(conn, "batata123", "pass")
    conn.close()
    
    app.run()  # Runs as a regular Flask server
