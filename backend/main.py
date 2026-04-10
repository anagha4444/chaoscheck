import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services.inject import router as inject_router
from services.monitor import start_monitoring
from services.logger import get_logs
from services.docker_utils import get_mongo_container, restart_container

from services.adaptive_healer import handle_incident_adaptively
from services.teacher import teach_system
from services.promotion import get_promotable_cases
from services.experience_store import load_experiences

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(inject_router)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_monitoring())

@app.get("/")
def home():
    return {"status": "Chaos Healer running"}

@app.get("/logs")
def logs():
    return get_logs()

@app.get("/experiences")
def experiences():
    return load_experiences()

@app.get("/promotion-candidates")
def promotion_candidates():
    return get_promotable_cases()

@app.post("/auto-heal")
def auto_heal():
    container = get_mongo_container()
    if container:
        container.reload()
        if container.status != "running":
            success = restart_container(container)
            if success:
                return {"status": "Mongo was DOWN → restarted"}
            else:
                return {"status": "Failed to restart Mongo"}
    return {"status": "Mongo is healthy or not found"}

@app.post("/adaptive-heal")
def adaptive_heal(data: dict):
    return handle_incident_adaptively(data)

@app.post("/teach-fix")
def teach_fix(data: dict):
    incident = data.get("incident", {})
    action_id = data.get("action_id")

    if not action_id:
        return {"status": "error", "message": "action_id is required"}

    return teach_system(incident, action_id)
@app.get("/status")
def status():
    container = get_mongo_container()
    mongo_status = "down"

    if container:
        try:
            container.reload()
            mongo_status = "healthy" if container.status == "running" else "down"
        except Exception:
            mongo_status = "down"

    return {
        "mongo": mongo_status,
        "backend": "healthy"
    }