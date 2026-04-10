from services.context_builder import build_context
from services.bandit import choose_action
from services.action_executor import execute_action
from services.action_catalog import ACTION_CATALOG
from services.experience_store import create_experience, save_experience
from services.reward import compute_reward
from services.verifier import verify_recovery
from services.logger import add_log


def get_candidate_actions(context):
    # Known Mongo-style incidents
    if context["has_mongodb"] or context["symptom"] in ["container_down", "db_unreachable"]:
        return ["restart_mongodb", "run_diagnostics", "ask_human"]

    # Known port incidents
    if context["has_eaddrinuse"]:
        return ["kill_port_3000", "run_diagnostics", "ask_human"]

    # Known memory incidents
    if context["has_memory"]:
        return ["restart_app", "run_diagnostics", "ask_human"]

    # Unknown incidents: allow broader learning
    return ["restart_app", "restart_mongodb", "run_diagnostics", "ask_human"]


def handle_incident_adaptively(incident: dict):
    context = build_context(incident)
    candidate_actions = get_candidate_actions(context)

    add_log(
        f"Adaptive analysis started for symptom={context['symptom']} service={context['service']}",
        log_type="warning",
        source="adaptive-healer"
    )

    action_id, scores, mode = choose_action(context, candidate_actions)
    chosen_confidence = scores[action_id]["confidence"]

    # If confidence is too low, ask human
    if action_id == "ask_human" or chosen_confidence < 0.30:
        add_log(
            f"No trusted playbook match. Needs operator guidance. Candidates={candidate_actions}",
            log_type="warning",
            source="adaptive-healer"
        )
        return {
            "status": "needs_human",
            "context": context,
            "scores": scores,
            "candidate_actions": candidate_actions,
            "mode": mode
        }

    success, message = execute_action(action_id)
    verified = verify_recovery(incident.get("service", "unknown"))
    risk = ACTION_CATALOG[action_id]["risk"]
    reward = compute_reward(success, verified, risk)

    exp = create_experience(
        context=context,
        action_id=action_id,
        success=(success and verified),
        reward=reward,
        source="bandit"
    )
    save_experience(exp)

    add_log(
        f"Adaptive healer executed {action_id} | success={success} verified={verified} reward={reward}",
        log_type="info" if success and verified else "warning",
        source="adaptive-healer"
    )

    return {
        "status": "executed",
        "action_id": action_id,
        "mode": mode,
        "scores": scores,
        "success": success,
        "verified": verified,
        "message": message
    }