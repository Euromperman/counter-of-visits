import socket
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify(message="Hello DevOps", host=socket.gethostname())

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
