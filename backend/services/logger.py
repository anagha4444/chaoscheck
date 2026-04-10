from datetime import datetime
from typing import List, Dict

# Centralized in-memory log storage
_logs: List[Dict] = []

def add_log(message: str, log_type: str = "info", source: str = "system"):
    """
    Appends a structured log entry to the in-memory log list.
    `log_type` is conventionally 'info', 'warning', or 'error'
    """
    new_log = {
        "message": message,
        "type": log_type,
        "source": source,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    # Insert at the beginning so the newest is first, or standard append
    _logs.insert(0, new_log)

def get_logs() -> List[Dict]:
    """
    Returns the list of logs.
    """
    return _logs
