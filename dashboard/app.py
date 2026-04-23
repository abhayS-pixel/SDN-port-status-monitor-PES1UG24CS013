from __future__ import annotations

import json
import os
from flask import Flask, render_template

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
STATUS_FILE = os.path.join(BASE_DIR, "logs", "current_status.json")
ALERT_FILE = os.path.join(BASE_DIR, "logs", "alerts.log")


def read_status():
    if not os.path.exists(STATUS_FILE):
        return {"ports": [], "recent_events": []}
    with open(STATUS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def read_alerts():
    if not os.path.exists(ALERT_FILE):
        return []
    with open(ALERT_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines() if line.strip()][-10:][::-1]


@app.route("/")
def index():
    data = read_status()
    alerts = read_alerts()
    return render_template(
        "index.html",
        ports=data.get("ports", []),
        recent_events=data.get("recent_events", []),
        alerts=alerts,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
