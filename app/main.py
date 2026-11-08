
import socket

import redis
from flask import Flask, jsonify

app = Flask(__name__)

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)


@app.route("/")
def home():
    return jsonify(
        message="Hello DevOps",
        host=socket.gethostname()
    )


@app.route("/visits")
def visits():
    count = redis_client.incr("visits")
    return jsonify(visits=count)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
