def build_context(incident: dict):
    error_text = (incident.get("error_log") or "").lower()
    service = incident.get("service", "unknown")
    symptom = incident.get("symptom", "unknown")
    container_status = incident.get("container_status", "unknown")
    source = incident.get("source", "unknown")

    return {
        "service": service,
        "symptom": symptom,
        "has_error_log": int(bool(error_text.strip())),
        "has_connection_refused": int("connection refused" in error_text),
        "has_mongodb": int("mongodb" in error_text or service == "mongodb"),
        "has_eaddrinuse": int("eaddrinuse" in error_text),
        "has_memory": int("memory" in error_text),
        "container_running": int(container_status == "running"),
        "source_monitor": int(source == "monitor"),
        "source_user": int(source == "user"),
    }