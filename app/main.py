from fastapi import FastAPI
from app.api import graph, challenges, keywords, admin


app = FastAPI(title="STEMgraph Challenge API", version="1.0.1")

app.include_router(graph.router)
app.include_router(challenges.router)
app.include_router(keywords.router)
app.include_router(admin.router)

@app.get("/healthcheck", tags=["Admin/Health Check"])
def healthcheck() -> dict[str, str]:
    return {"status": "ok", "message": "API is running and connected to Neo4j"}
