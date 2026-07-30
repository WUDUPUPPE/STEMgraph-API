from fastapi import APIRouter
from app.service.neo4j_client import run_query
    
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
def get_subgraph(start: str, end: str):
    query = """
    MATCH path = shortestPath(
        (a:Challenge {uuid: $start})-[:BUILDS_ON*]-(b:Challenge {uuid: $end})
    )
    RETURN path
    """
    return run_query(query, {"start": start, "end": end})