from services.context_builder import build_context
from services.action_executor import execute_action
from services.action_catalog import ACTION_CATALOG
from services.experience_store import create_experience, save_experience
from services.reward import compute_reward
from services.verifier import verify_recovery
from services.logger import add_log


def teach_system(incident: dict, action_id: str):
    if action_id not in ACTION_CATALOG:
        return {
            "status": "error",
            "message": f"Unknown action_id: {action_id}"
        }

    context = build_context(incident)

    success, message = execute_action(action_id)
    verified = verify_recovery(incident.get("service", "unknown"))
    risk = ACTION_CATALOG[action_id]["risk"]
    reward = compute_reward(success, verified, risk)

    exp = create_experience(
        context=context,
        action_id=action_id,
        success=(success and verified),
        reward=reward,
        source="user"
    )
    save_experience(exp)

    add_log(
        f"System taught with action {action_id} | success={success} verified={verified}",
        log_type="info" if success and verified else "warning",
        source="teaching"
    )

    return {
        "status": "taught",
        "action_id": action_id,
        "success": success,
        "verified": verified,
        "message": message
    }