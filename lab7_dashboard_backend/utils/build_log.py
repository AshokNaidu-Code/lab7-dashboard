import json
from datetime import datetime
from pathlib import Path

log_file = Path("build_log.json")

def add_build_entry(status, message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    entry = {"timestamp": timestamp, "status": status, "message": message}

    if log_file.exists():
        with log_file.open("r", encoding="utf-8") as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append(entry)

    with log_file.open("w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2)

def get_build_history():
    if log_file.exists():
        with log_file.open("r", encoding="utf-8") as f:
            return json.load(f)
    return []

def clear_history():
    if log_file.exists():
        log_file.write_text("[]")