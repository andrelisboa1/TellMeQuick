from flask import Flask, render_template, request
import threading
import time
import subprocess
import requests

app = Flask(__name__)
has_launched_ngrok = False

def launch_ngrok():
    time.sleep(4)  # Wait for 4 seconds
    subprocess.Popen(["sudo", "ngrok", "http", "5000"])  # Launch ngrok in a new process
    time.sleep(4)  # Wait for ngrok to initialize
    try:
        response = requests.get("http://localhost:4040/api/tunnels")  # Get ngrok tunnels
        tunnels = response.json().get("tunnels", [])
        public_url = next((tunnel["public_url"] for tunnel in tunnels if tunnel["proto"] == "https"), None)
        if public_url:
            print(f"Ngrok URL: {public_url}")
    except Exception as e:
        print(f"Error retrieving ngrok URL: {e}")

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
