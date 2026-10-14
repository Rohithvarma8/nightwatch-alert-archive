#!/usr/bin/env python3
"""Record active NWS alerts for California into archive/nws/."""

import hashlib
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

URL = "https://api.weather.gov/alerts/active?area=CA"
ARCHIVE = Path(__file__).resolve().parent / "archive" / "nws"


def fetch():
    user_agent = os.environ.get("NWS_USER_AGENT")
    if not user_agent:
        sys.exit("NWS_USER_AGENT is not set")
    req = urllib.request.Request(
        URL,
        headers={"User-Agent": user_agent, "Accept": "application/geo+json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP error {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        sys.exit(f"Request failed: {e.reason}")


def main():
    features = fetch().get("features", [])
    recorded_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    new = 0
    for feature in features:
        props = feature.get("properties", {})
        alert_id, sent = props.get("id"), props.get("sent")
        if not alert_id or not sent:
            continue
        day = sent[:10]  # YYYY-MM-DD from the ISO 8601 timestamp
        name = hashlib.sha1(alert_id.encode()).hexdigest()[:16] + ".json"
        path = ARCHIVE / day / name
        if path.exists():
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        feature["_recorded_at"] = recorded_at
        path.write_text(json.dumps(feature, indent=2) + "\n")
        new += 1
    print(f"active={len(features)} new={new}")


if __name__ == "__main__":
    main()
