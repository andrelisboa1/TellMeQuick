from flask import Flask, render_template, request
from flask_ngrok import run_with_ngrok, start_ngrok

app = Flask(__name__)

run_with_ngrok(app)  # Enable ngrok tunnel

@app.route("/")
def home():
    mode = request.args.get("mode", "light")
    return render_template("home.html", mode=mode)

@app.route("/about")
def about():
    mode = request.args.get("mode", "light")
    return render_template("about.html", mode=mode)

if __name__ == "__main__":
    app.run()
