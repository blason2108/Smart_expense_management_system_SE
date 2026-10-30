#!/usr/bin/env python3
"""Local smoke: committed demo records remain identical after restarting our own server process."""

import os
import subprocess
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
BASE = "http://127.0.0.1:8765"


def start():
    proc = subprocess.Popen(
        [sys.executable, "manage.py", "runserver", "127.0.0.1:8765", "--noreload"],
        cwd=ROOT / "smart-expense",
        env=os.environ.copy(),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    for _ in range(50):
        if proc.poll() is not None:
            raise RuntimeError(
                "Server failed to start; check config and free port 8765."
            )
        try:
            if requests.get(BASE + "/healthz/", timeout=1).status_code == 200:
                return proc
        except requests.RequestException:
            pass
        time.sleep(0.1)
    proc.terminate()
    proc.wait(timeout=10)
    raise RuntimeError("Server startup timed out.")


def main():
    password = os.environ.get("DEMO_PASSWORD")
    if not password:
        raise SystemExit("Set DEMO_PASSWORD and seed_demo first.")
    proc = None
    try:
        proc = start()
        session = requests.Session()
        session.get(BASE + "/accounts/login/", timeout=5)
        result = session.post(
            BASE + "/accounts/login/",
            data={
                "username": "demo",
                "password": password,
                "csrfmiddlewaretoken": session.cookies["csrftoken"],
            },
            timeout=5,
        )
        if "Logout" not in result.text:
            raise RuntimeError("Login failed.")
        url = BASE + "/reports/?month=2026-10&export=csv"
        before = session.get(url, timeout=5)
        if not before.headers.get("Content-Type", "").startswith("text/csv"):
            raise RuntimeError("Expected authenticated CSV export.")
        proc.terminate()
        proc.wait(timeout=10)
        proc = None
        proc = start()
        after = session.get(url, timeout=5)
        if before.content != after.content:
            raise RuntimeError("Committed report changed across restart.")
        print(
            "PASS: authenticated October CSV data and session preserved across local process restart."
        )
    finally:
        if proc is not None and proc.poll() is None:
            proc.terminate()
            proc.wait(timeout=10)


if __name__ == "__main__":
    main()
