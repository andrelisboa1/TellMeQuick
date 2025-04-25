from flask import Flask, render_template, request
import threading
import time
import os
import requests

app = Flask(__name__)
has_launched_ngrok = False

def launch_ngrok():
    time.sleep(6)  # Wait for 4 seconds
    os.system("sudo ngrok http 5000 > ngrok.log 2>&1 &")  # Launch ngrok in a new process
    time.sleep(4)  # Wait for ngrok to initialize
    try:
        with open("ngrok.log", "r") as log_file:
            for line in log_file:
                if "https://" in line or "http://" in line:
                    public_url = line.split(" ")[-1].strip()
                    print(f"Ngrok URL: {public_url}")  # Display the public URL
                    break
    except Exception as e:
        print(f"Error reading ngrok log: {e}")

@app.route("/")
def home():
    mode = request.args.get("mode", "light")
    
    return render_template("home.html", mode=mode)

@app.route("/about")
def about():
    mode = request.args.get("mode", "light")
    return render_template("about.html", mode=mode)

if __name__ == "__main__":
    if not has_launched_ngrok:
        has_launched_ngrok = True
        threading.Thread(target=launch_ngrok, daemon=True).start()
    app.run()  # Runs as a regular Flask server
