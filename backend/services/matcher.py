def find_fix(error_log):
    error = error_log.lower()

    if "mongodb" in error or "connection refused" in error:
        return {
            "service": "mongodb",
            "action": "restart",
            "command": "echo Restart MongoDB"
        }

    if "eaddrinuse" in error:
        return {
            "service": "port",
            "action": "kill_port",
            "command": "echo Kill port 3000"
        }

    if "memory" in error:
        return {
            "service": "app",
            "action": "restart",
            "command": "echo Restart app"
        }

    return None