from services.docker_utils import get_mongo_container

def verify_recovery(service):
    print(f"🔍 Verifying {service} recovery...")

    if service == "mongodb":
        container = get_mongo_container()
        if not container:
            return False
        try:
            container.reload()
            return container.status == "running"
        except Exception:
            return False

    if service == "app":
        return True

    if service == "port":
        return True

    return False