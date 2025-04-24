from flask import Flask, render_template, request
import threading
import time
import subprocess

app = Flask(__name__)
has_launched_ngrok = False

def launch_ngrok():
    time.sleep(5)  # Wait for 5 seconds
    subprocess.Popen(["ngrok", "http", "5000"])  # Launch ngrok in a new process

@app.route("/")
def home():
    global has_launched_ngrok
    mode = request.args.get("mode", "light")
    if not has_launched_ngrok:
        has_launched_ngrok = True
        threading.Thread(target=launch_ngrok, daemon=True).start()
    return render_template("home.html", mode=mode)

@app.route("/about")
def about():
    mode = request.args.get("mode", "light")
    return render_template("about.html", mode=mode)

if __name__ == "__main__":
    app.run()  # Runs as a regular Flask server
