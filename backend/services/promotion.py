from collections import defaultdict
from services.experience_store import load_experiences


def get_promotable_cases(min_attempts=3, min_success_rate=0.8):
    experiences = load_experiences()
    grouped = defaultdict(list)

    for exp in experiences:
        ctx = exp["context"]
        key = (
            ctx["service"],
            ctx["symptom"],
            ctx["has_connection_refused"],
            ctx["has_mongodb"],
            ctx["has_eaddrinuse"],
            ctx["has_memory"],
            exp["action_id"]
        )
        grouped[key].append(exp)

    promotable = []

    for key, rows in grouped.items():
        attempts = len(rows)
        successes = sum(1 for r in rows if r["success"])
        success_rate = successes / attempts if attempts else 0

        if attempts >= min_attempts and success_rate >= min_success_rate:
            promotable.append({
                "key": key,
                "attempts": attempts,
                "success_rate": round(success_rate, 3)
            })

    return promotable