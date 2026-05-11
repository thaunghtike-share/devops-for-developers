from flask import Flask
import os

app = Flask(__name__)

APP_NAME = os.getenv("APP_NAME", "Hello Docker World")

@app.route("/")
def home():
    return APP_NAME

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)