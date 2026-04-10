from services.docker_utils import get_mongo_container, restart_container
from services.logger import add_log


def action_restart_mongodb():
    container = get_mongo_container()
    if not container:
        add_log("MongoDB container not found", log_type="error", source="action-catalog")
        return False, "MongoDB container not found"

    success = restart_container(container)
    if success:
        add_log("MongoDB restart action succeeded", log_type="info", source="action-catalog")
        return True, "MongoDB restarted"
    else:
        add_log("MongoDB restart action failed", log_type="error", source="action-catalog")
        return False, "MongoDB restart failed"


def action_restart_app():
    add_log("App restart simulated", log_type="warning", source="action-catalog")
    return True, "App restart simulated"


def action_kill_port_3000():
    add_log("Port 3000 cleanup simulated", log_type="warning", source="action-catalog")
    return True, "Port 3000 cleanup simulated"


def action_run_diagnostics():
    add_log("Diagnostics executed", log_type="info", source="action-catalog")
    return True, "Diagnostics completed"


ACTION_CATALOG = {
    "restart_mongodb": {
        "handler": action_restart_mongodb,
        "risk": "low",
        "description": "Restart MongoDB container"
    },
    "restart_app": {
        "handler": action_restart_app,
        "risk": "medium",
        "description": "Restart application service"
    },
    "kill_port_3000": {
        "handler": action_kill_port_3000,
        "risk": "medium",
        "description": "Kill process occupying port 3000"
    },
    "run_diagnostics": {
        "handler": action_run_diagnostics,
        "risk": "none",
        "description": "Run safe diagnostics only"
    },
    "ask_human": {
        "handler": None,
        "risk": "none",
        "description": "Ask operator/user for help"
    }
}