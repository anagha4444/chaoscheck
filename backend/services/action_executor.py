from services.action_catalog import ACTION_CATALOG


def execute_action(action_id: str):
    action = ACTION_CATALOG.get(action_id)
    if not action:
        return False, f"Unknown action: {action_id}"

    handler = action.get("handler")
    if not handler:
        return False, "No handler available for this action"

    return handler()