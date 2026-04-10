from fastapi import APIRouter
from services.docker_utils import get_mongo_container, stop_container
from services.logger import add_log
from services.healer import trigger_healer

router = APIRouter()

@router.post("/inject-mongodb")
def inject_mongodb():
    container = get_mongo_container()
    if container:
        add_log("Injected manual database failure", log_type="warning", source="user")
        stop_container(container)
        add_log("MongoDB DOWN detected", log_type="error", source="monitor-agent")
        return {"status": "mongodb failure injected"}
    return {"status": "mongodb container not found"}


@router.post("/inject-port")
def inject_port():
    error = "Error: listen EADDRINUSE: address already in use :::3000"
    add_log("Injected known port conflict: EADDRINUSE on port 3000", log_type="error", source="monitor-agent")
    trigger_healer(error)
    return {"status": "port error injected", "error": error}


@router.post("/inject-memory")
def inject_memory():
    error = "FATAL: JavaScript heap out of memory"
    add_log("Injected known memory pressure incident", log_type="error", source="monitor-agent")
    trigger_healer(error)
    return {"status": "memory error injected", "error": error}


@router.post("/inject-unknown")
def inject_unknown():
    error = "CRITICAL: cache layer failure - unknown signature"
    incident = {
        "service": "app",
        "error_log": error,
        "symptom": "unknown_failure",
        "container_status": "unknown",
        "source": "monitor"
    }

    add_log(error, log_type="error", source="monitor-agent")
    add_log("No playbook match found. Entering adaptive mode.", log_type="warning", source="adaptive-healer")

    return {
        "status": "unknown injected",
        "incident": incident
    }