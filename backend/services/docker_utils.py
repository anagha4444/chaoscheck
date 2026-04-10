import docker
from typing import Optional

def get_docker_client():
    """Initializes and returns the Docker client."""
    try:
        return docker.from_env()
    except Exception as e:
        print(f"Error connecting to Docker: {e}")
        return None

def get_mongo_container(client=None) -> Optional[docker.models.containers.Container]:
    """
    Dynamically searches for the MongoDB container.
    Returns the container object if found, otherwise None.
    """
    if not client:
        client = get_docker_client()
    if not client:
        return None

    try:
        # Instead of just running status='running', get all containers to check correctly
        # because the monitor needs to be able to find it even when it's stopped/exited.
        containers = client.containers.list(all=True)
        for c in containers:
            # Check by container image name
            tags = c.image.tags
            if any("mongo" in tag for tag in tags):
                return c
            # Fallback: check by container name
            if "database" in c.name or "mongo" in c.name:
                return c
    except Exception as e:
        print(f"Failed to list containers: {e}")

    return None

def restart_container(container) -> bool:
    """Restarts a container and verifies it started successfully."""
    try:
        container.restart()
        # Reload container state after restart
        container.reload()
        return container.status == "running"
    except Exception as e:
        print(f"Failed to restart container: {e}")
        return False

def stop_container(container) -> bool:
    """Stops a container."""
    try:
        if container.status == "running":
            container.stop()
        return True
    except Exception as e:
        print(f"Failed to stop container: {e}")
        return False
