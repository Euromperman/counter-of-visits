import logging
import os
import socket
import sys

import redis
from flask import Flask, jsonify, request

app = Flask(__name__)

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", "6379")),
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


@app.route("/health")
def health():
    try:
        redis_client.ping()
        return jsonify(status="ok"), 200
    except redis.RedisError:
        return jsonify(status="error"), 503



logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout
)

logger = logging.getLogger(__name__)

@app.before_request
def log_request():
    logger.info("HTTP %s %s", request.method, request.path)






if __name__ == "__main__":
    port = int(os.getenv("APP_PORT", "5000"))
    app.run(host="0.0.0.0", port=port)