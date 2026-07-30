from fastapi import APIRouter
from pydantic import BaseModel, Field
from app.service.neo4j_client import run_query

class SubgraphResponse(BaseModel):
    uuid: str
    title: str 
    keywords: list[str] = Field(default_factory=list)
    
router = APIRouter()

@router.get("/graph", tags=["Graph-Info"])
def get_graph():
    query = """
    MATCH (c:Challenge)
    OPTIONAL MATCH (c)-[r:BUILDS_ON]->(dep:Challenge)
    RETURN c, r, dep
    """
    return run_query(query)

@router.get("/subgraph", tags=["Graph-Info"])
def get_subgraph(start: str, end: str) -> SubgraphResponse:
    query = """
    MATCH path = shortestPath(
        (a:Challenge {uuid: $start})-[:BUILDS_ON*]-(b:Challenge {uuid: $end})
    )
    RETURN path
    """
    return run_query(query, {"start": start, "end": end})