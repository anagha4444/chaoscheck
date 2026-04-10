import asyncio
from services.logger import add_log
from services.docker_utils import get_mongo_container, restart_container

async def start_monitoring():
    """
    Background worker that indefinitely monitors the database container.
    """
    print("Initiating background monitoring loop...")
    while True:
        try:
            container = get_mongo_container()
            if container:
                # Reload container metadata to get the latest status
                container.reload()
                if container.status != "running":
                    # Detected an offline database!
                    add_log("MongoDB DOWN detected", log_type="error", source="monitor-agent")
                    
                    # Trigger the healing function
                    add_log("Restarting MongoDB container...", log_type="warning", source="auto-healer")
                    success = restart_container(container)
                    
                    # Wait briefly to ensure state transitions properly
                    await asyncio.sleep(2)
                    
                    if success:
                        add_log("MongoDB successfully healed", log_type="info", source="auto-healer")
                    else:
                        add_log("Healing failed", log_type="error", source="auto-healer")
            else:
                 # Didn't find container
                 # Commenting out so it doesn't spam missing container logs during dev
                 # print("MongoDB container not found. Is it initialized?")
                 pass
                
        except Exception as e:
            print(f"Monitor encountered an error: {e}")
            
        # Polling interval
        await asyncio.sleep(5)