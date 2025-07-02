import json
from datetime import datetime
from pathlib import Path

log_file = Path("build_log.json")

def add_build_entry(status: str, message: str):
    entry = {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "status": status,
        "message": message
    }

    logs = get_build_history()
    logs.append(entry)
    logs = logs[-10:]  # Keep only the latest 10
    log_file.write_text(json.dumps(logs, indent=2))

def get_build_history():
    if log_file.exists():
        return json.loads(log_file.read_text())
    return []

def clear_history():
    if log_file.exists():
        log_file.write_text("[]")
    
