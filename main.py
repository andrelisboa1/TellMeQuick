from flask import Flask, render_template, request
import threading
import time
import os
import requests

app = Flask(__name__)
has_launched_ngrok = False

def launch_ngrok():
    time.sleep(6)  # Wait for 4 seconds
    print("_ Configuring token...")
    os.system("sudo ngrok config add-authtoken 2vpZrJfJIS84wuDoUH2AGRjZPpV_6VtxX228YWdUEovkiT4fS &")
    time.sleep(4)
    print("_ Launching ngrok tunnel...")
    os.system("sudo ngrok http 5000 > ./ng.txt &")  # Launch ngrok in a new process
    for i in range(6):
        print(f"_ _ {i+1} / 6 seconds...")
        time.sleep(1)  # Wait for ngrok to initialize
    print("_ Displaying ngrok info...")
    try:
        with open("./ng.txt", "r") as log_file:
            print("NGROK FILE")
            c = 0
            for index, line in enumerate(log_file):
                print(f"_ Line {i+1}\n{line}")
                c += 1
            print(f"(Line count: {c})")
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
