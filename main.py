from flask import Flask, render_template, request, redirect, url_for
import sqlite3 as sql
import threading
import time
import os
import db

app = Flask(__name__)

@app.route("/")
def home():
    conn = sql.connect(db.db_filename)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM user")
    users = cursor.fetchall()
    conn.close()
    return render_template("home.html", users=users)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/users")
def users():
    conn = sql.connect(db.db_filename)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM user")
    users = cursor.fetchall()
    conn.close()
    return render_template("users.html", users=users)

@app.route("/chat")
def chat():
    logged_in_user = "batata123"  # Assume this user is logged in
    conn = sql.connect(db.db_filename)
    cursor = conn.cursor()

    # Fetch user IDs for batata123 and cenoura456
    cursor.execute("SELECT id FROM user WHERE username = ?", (logged_in_user,))
    logged_in_user_id = cursor.fetchone()[0]
    cursor.execute("SELECT id FROM user WHERE username = ?", ("cenoura456",))
    other_user_id = cursor.fetchone()[0]

    # Fetch messages between the two users
    messages = db.get_messages_between_users(conn, logged_in_user_id, other_user_id)
    conn.close()

    return render_template("chat.html", user=logged_in_user, user_id=logged_in_user_id, messages=messages)

@app.route("/send_message", methods=["POST"])
def send_message():
    logged_in_user = "batata123"  # Assume this user is logged in
    message_content = request.form["message"]

    conn = sql.connect(db.db_filename)
    cursor = conn.cursor()

    # Fetch user IDs for batata123 and cenoura456
    cursor.execute("SELECT id FROM user WHERE username = ?", (logged_in_user,))
    logged_in_user_id = cursor.fetchone()[0]
    cursor.execute("SELECT id FROM user WHERE username = ?", ("cenoura456",))
    other_user_id = cursor.fetchone()[0]

    # Add the message to the database
    db.add_message(conn, logged_in_user_id, other_user_id, message_content)
    conn.close()

    return redirect(url_for("chat"))

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
    db.create_user(conn, "cenoura456", "pass2")
    conn.close()
    
    app.run()  # Runs as a regular Flask server
