import os
import socket
from pathlib import Path

from flask import Flask, jsonify
from redis import Redis
from redis.exceptions import RedisError

app = Flask(__name__)

DATA_DIR = Path(os.environ.get("DATA_DIR", "/data"))
COUNT_FILE = DATA_DIR / "count.txt"


def redis_client():
    host = os.environ.get("REDIS_HOST")
    if not host:
        return None
    return Redis(
        host=host,
        port=int(os.environ.get("REDIS_PORT", "6379")),
        decode_responses=True,
        socket_connect_timeout=1,
    )


def backend_name():
    return "redis" if os.environ.get("REDIS_HOST") else "file"


def read_file_count():
    return int(COUNT_FILE.read_text()) if COUNT_FILE.exists() else 0


@app.get("/")
def index():
    return jsonify(
        hostname=socket.gethostname(),
        message=os.environ.get("MESSAGE", "Hello from the Docker field manual!"),
        counter_backend=backend_name(),
    )


@app.get("/count")
def get_count():
    client = redis_client()
    if client:
        try:
            return jsonify(count=int(client.get("visits") or 0), backend="redis")
        except RedisError as exc:
            return jsonify(error=str(exc), backend="redis"), 503
    return jsonify(count=read_file_count(), backend="file")


@app.post("/count")
def increment_count():
    client = redis_client()
    if client:
        try:
            return jsonify(count=client.incr("visits"), backend="redis")
        except RedisError as exc:
            return jsonify(error=str(exc), backend="redis"), 503
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    count = read_file_count() + 1
    COUNT_FILE.write_text(str(count))
    return jsonify(count=count, backend="file")


@app.get("/healthz")
def healthz():
    client = redis_client()
    if client:
        try:
            client.ping()
        except RedisError as exc:
            return jsonify(status="unhealthy", dependency="redis", error=str(exc)), 503
    return jsonify(status="healthy", backend=backend_name())


@app.get("/config")
def config():
    return jsonify(
        message=os.environ.get("MESSAGE"),
        data_dir=str(DATA_DIR),
        redis_host=os.environ.get("REDIS_HOST"),
        redis_port=os.environ.get("REDIS_PORT", "6379"),
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
