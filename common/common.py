"""Shared helpers for all chains. Read-only / confirmation use at step 1.

Loads the target URL from the repo-root .env (JUICE_SHOP_URL) and gives every
chain a consistent HTTP session plus a small evidence logger so findings land
in evidence/<chain>/ in a uniform shape.
"""
from __future__ import annotations
import json
import os
import pathlib
import datetime
import requests

ROOT = pathlib.Path(__file__).resolve().parents[1]


def target_url() -> str:
    env = ROOT / ".env"
    url = "http://localhost:3000"
    if env.exists():
        for line in env.read_text().splitlines():
            line = line.strip()
            if line.startswith("JUICE_SHOP_URL="):
                url = line.split("=", 1)[1].strip()
    return os.environ.get("JUICE_SHOP_URL", url)


def session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": "26CSCN26H-lab/step1"})
    return s


def save_evidence(chain: str, name: str, data: dict) -> pathlib.Path:
    """Write a timestamped JSON evidence record under evidence/<chain>/."""
    out_dir = ROOT / "evidence" / chain
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    path = out_dir / f"{name}-{ts}.json"
    record = {"captured_at": ts, "target": target_url(), **data}
    path.write_text(json.dumps(record, indent=2))
    print(f"[evidence] {path.relative_to(ROOT)}")
    return path


def check_target(s: requests.Session) -> bool:
    url = target_url()
    try:
        r = s.get(url, timeout=5)
        print(f"[target] {url} -> HTTP {r.status_code}")
        return r.status_code < 500
    except requests.RequestException as e:
        print(f"[target] {url} unreachable: {e}")
        print("        Start it with: docker compose up -d")
        return False
