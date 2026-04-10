import json
import os
from datetime import datetime

DB_FILE = "experience_db.json"


def load_experiences():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as f:
        return json.load(f)


def save_experience(experience: dict):
    data = load_experiences()
    data.append(experience)
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)


def create_experience(context, action_id, success, reward, source="system"):
    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "context": context,
        "action_id": action_id,
        "success": success,
        "reward": reward,
        "source": source
    }