import random
from services.experience_store import load_experiences

FEATURE_KEYS = [
    "service",
    "symptom",
    "has_error_log",
    "has_connection_refused",
    "has_mongodb",
    "has_eaddrinuse",
    "has_memory",
    "container_running",
    "source_monitor",
    "source_user",
]


def context_similarity(c1, c2):
    score = 0
    for key in FEATURE_KEYS:
        if c1.get(key) == c2.get(key):
            score += 1
    return score / len(FEATURE_KEYS)


def score_actions(context, candidate_actions):
    experiences = load_experiences()
    results = {}

    for action_id in candidate_actions:
        weighted_reward = 0.0
        total_weight = 0.0
        count = 0

        for exp in experiences:
            if exp["action_id"] != action_id:
                continue

            sim = context_similarity(context, exp["context"])
            if sim <= 0:
                continue

            weighted_reward += sim * exp["reward"]
            total_weight += sim
            count += 1

        if total_weight == 0:
            results[action_id] = {
                "score": 0.5,
                "count": 0,
                "confidence": 0.0
            }
        else:
            score = weighted_reward / total_weight
            confidence = max(0.0, min(1.0, score / 10.0)) * min(1.0, count / 5)
            results[action_id] = {
                "score": round(score, 3),
                "count": count,
                "confidence": round(confidence, 3)
            }

    return results


def choose_action(context, candidate_actions, epsilon=0.1):
    scores = score_actions(context, candidate_actions)

    if random.random() < epsilon:
        action_id = random.choice(candidate_actions)
        return action_id, scores, "explore"

    best = max(candidate_actions, key=lambda a: scores[a]["score"])
    return best, scores, "exploit"