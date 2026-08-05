from fastapi import FastAPI
from pydantic import BaseModel
from app.api import graph, keywords, admin, list

class HealthcheckResponse(BaseModel):
    status: str
    message: str

app = FastAPI(title="STEMgraph API", version="2.0.0")

app.include_router(graph.router)
app.include_router(list.router)
app.include_router(keywords.router)
app.include_router(admin.router)

@app.get("/healthcheck", tags=["Admin/Health Check"])
def healthcheck() -> HealthcheckResponse:
    return HealthcheckResponse(
        status="ok", message="API is healthy and running"
        )
