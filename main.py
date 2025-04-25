from flask import Flask, render_template, request
import threading
import time
import os
import requests

app = Flask(__name__)

@app.route("/")
def home():
    mode = request.args.get("mode", "light")
    return render_template("home.html", mode=mode)

@app.route("/about")
def about():
    mode = request.args.get("mode", "light")
    return render_template("about.html", mode=mode)

if __name__ == "__main__":
    app.run()  # Runs as a regular Flask server
