from __future__ import annotations

import csv
import json
import os
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from urllib.parse import urlparse, parse_qs

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LOG_DIR = os.path.join(BASE_DIR, "logs")

CSV_FILE = os.path.join(LOG_DIR, "port_status_log.csv")
ALERT_FILE = os.path.join(LOG_DIR, "alerts.log")
STATUS_FILE = os.path.join(LOG_DIR, "current_status.json")

port_states = {}
recent_events = []


def ensure_files():
    os.makedirs(LOG_DIR, exist_ok=True)

    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp",
                "switch",
                "port_no",
                "port_name",
                "reason",
                "state"
            ])

    if not os.path.exists(ALERT_FILE):
        open(ALERT_FILE, "w", encoding="utf-8").close()

    if not os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "ports": [],
                    "recent_events": []
                },
                f,
                indent=2
            )


def append_csv(event):
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            event["timestamp"],
            event["switch"],
            event["port_no"],
            event["port_name"],
            event["reason"],
            event["state"]
        ])


def append_alert(message):
    with open(ALERT_FILE, "a", encoding="utf-8") as f:
        f.write(message + "\n")


def save_status():
    ports = []

    for _, info in sorted(port_states.items()):
        ports.append(info)

    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(
            {
                "ports": ports,
                "recent_events": recent_events[:10]
            },
            f,
            indent=2
        )


def add_event(state, reason, switch, port_no, port_name):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    event = {
        "timestamp": timestamp,
        "switch": switch,
        "port_no": port_no,
        "port_name": port_name,
        "reason": reason,
        "state": state,
        "last_updated": timestamp
    }

    port_states[(switch, port_no)] = event
    recent_events.insert(0, event)

    append_csv(event)
    save_status()

    print(
        f"Port event -> switch={switch} "
        f"port={port_no} "
        f"name={port_name} "
        f"reason={reason} "
        f"state={state}"
    )

    if state in {"DOWN", "BLOCKED", "LINK_DOWN"}:
        alert = (
            f"ALERT [{timestamp}] "
            f"switch={switch} "
            f"port={port_no} "
            f"name={port_name} "
            f"state={state} "
            f"reason={reason}"
        )

        print(alert)
        append_alert(alert)


class DemoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)

        switch = query.get("switch", ["s1"])[0]
        port_no = int(query.get("port", [1])[0])
        port_name = query.get("name", [f"{switch}-eth{port_no}"])[0]

        if parsed.path == "/up":
            add_event("UP", "MANUAL", switch, port_no, port_name)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(
                f"{switch} port {port_no} ({port_name}) marked UP".encode()
            )

        elif parsed.path == "/down":
            add_event("DOWN", "MANUAL", switch, port_no, port_name)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(
                f"{switch} port {port_no} ({port_name}) marked DOWN".encode()
            )

        elif parsed.path == "/":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(
                b"Port Status Monitoring Tool running.\n"
                b"Use:\n"
                b"/down?switch=s1&port=1\n"
                b"/up?switch=s2&port=2\n"
            )

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Invalid URL")

    def log_message(self, format, *args):
        return


def run_server():
    server = HTTPServer(("0.0.0.0", 8080), DemoHandler)

    print("Controller simulator running on http://127.0.0.1:8080")
    print("Available switches and ports:")
    print("  s1 -> s1-eth1, s1-eth2")
    print("  s2 -> s2-eth1, s2-eth2")
    print("  s3 -> s3-eth1, s3-eth2")
    print()
    print("Examples:")
    print('  curl "http://127.0.0.1:8080/down?switch=s1&port=1"')
    print('  curl "http://127.0.0.1:8080/down?switch=s2&port=2"')
    print('  curl "http://127.0.0.1:8080/up?switch=s3&port=1"')
    print()

    server.serve_forever()


if __name__ == "__main__":
    ensure_files()

    print("Port Status Monitoring Tool started")
    print("Initializing 3 switches with 2 ports each...")

    add_event("UP", "INITIAL", "s1", 1, "s1-eth1")
    add_event("UP", "INITIAL", "s1", 2, "s1-eth2")

    add_event("UP", "INITIAL", "s2", 1, "s2-eth1")
    add_event("UP", "INITIAL", "s2", 2, "s2-eth2")

    add_event("UP", "INITIAL", "s3", 1, "s3-eth1")
    add_event("UP", "INITIAL", "s3", 2, "s3-eth2")

    Thread(target=run_server, daemon=True).start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nStopped.")
