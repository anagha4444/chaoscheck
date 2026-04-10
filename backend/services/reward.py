def compute_reward(success: bool, verified: bool, risk: str):
    if success and verified:
        base = 10
    elif success and not verified:
        base = 2
    else:
        base = -5

    penalty = {
        "none": 0,
        "low": 0,
        "medium": -1,
        "high": -3
    }.get(risk, -1)

    return base + penalty