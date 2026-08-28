import os
import socket
from pathlib import Path

from flask import Flask, jsonify

app = Flask(__name__)

DATA_DIR = Path(os.environ.get("DATA_DIR", "/data"))
COUNT_FILE = DATA_DIR / "count.txt"
HEALTH_FLAG_FILE = Path("/tmp/unhealthy")

CONFIG_DIR = Path("/etc/config")
SECRET_DIR = Path("/etc/secret")


@app.route("/")
def index():
    return jsonify(
        hostname=socket.gethostname(),
        app_version=os.environ.get("APP_VERSION", "v1"),
        message=os.environ.get("MESSAGE", "Hello from hello-app!"),
    )


@app.route("/healthz")
def healthz():
    if HEALTH_FLAG_FILE.exists():
        return jsonify(status="unhealthy"), 500
    return jsonify(status="ok")


@app.route("/toggle-health", methods=["POST"])
def toggle_health():
    if HEALTH_FLAG_FILE.exists():
        HEALTH_FLAG_FILE.unlink()
        return jsonify(status="healthy")
    HEALTH_FLAG_FILE.touch()
    return jsonify(status="unhealthy")


@app.route("/config")
def config():
    def read_dir(directory):
        if not directory.is_dir():
            return {}
        return {f.name: f.read_text().strip() for f in directory.iterdir() if f.is_file()}

    return jsonify(
        env={
            "APP_VERSION": os.environ.get("APP_VERSION"),
            "MESSAGE": os.environ.get("MESSAGE"),
            "GREETING_LANG": os.environ.get("GREETING_LANG"),
        },
        config_files=read_dir(CONFIG_DIR),
        secret_files=read_dir(SECRET_DIR),
    )


@app.route("/count", methods=["GET"])
def get_count():
    count = int(COUNT_FILE.read_text()) if COUNT_FILE.exists() else 0
    return jsonify(count=count)


@app.route("/count", methods=["POST"])
def increment_count():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    count = int(COUNT_FILE.read_text()) if COUNT_FILE.exists() else 0
    count += 1
    COUNT_FILE.write_text(str(count))
    return jsonify(count=count)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
