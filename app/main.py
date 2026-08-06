from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager
from app.api import graph, keywords, admin, list
from app.service.task_scheduler import create_stop_event, start_scheduler, stop_scheduler

class HealthcheckResponse(BaseModel):
    status: str
    message: str

app = FastAPI(title="STEMgraph API", version="2.1.0")

app.include_router(graph.router)
app.include_router(list.router)
app.include_router(keywords.router)
app.include_router(admin.router)

@asynccontextmanager
async def lifespan(app: FastAPI):
    stop_event = create_stop_event()
    scheduler_task = await start_scheduler(stop_event)

    yield
    await stop_scheduler(stop_event,scheduler_task)

@app.get("/healthcheck", tags=["Admin/Health Check"])
def healthcheck() -> HealthcheckResponse:
    return HealthcheckResponse(
        status="ok", message="API is healthy and running")