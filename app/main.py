from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager
from app.api import graph, keywords, admin, list
from app.service.task_scheduler import create_stop_event, start_scheduler, stop_scheduler
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="STEMgraph API", version="2.5.0")

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200"], 
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

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
    