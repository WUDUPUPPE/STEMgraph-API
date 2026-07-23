from fastapi import APIRouter
from app.service.neo4j_client import run_query

router = APIRouter()

@router.get("/challenges", tags=["Challenges"])
def get_all_challenges():
    query = "MATCH (c:Challenge) RETURN c"
    return run_query(query)

@router.get("/challenges/{id}/depends-on")
def get_challenge_dependencies(id: str, format: str ="list"):
    if format == "tree":
        query = """
        MATCH (c:Challenge {uuid:$id})-[:BUILDS_ON*]->(dep)
        RETURN dep
        """
    else:
        query = """
        MATCH (c:Challenge {uuid:$id})-[:BUILDS_ON]->(dep)
        RETURN dep
        """
    return run_query(query, {"id": id})

@router.get("/challenges/{id}/neighbors")
def get_challenge_neighbors(id: str):
    query = """
    MATCH (c:Challenge {uuid:$id})-[:BUILDS_ON]-(n)
    RETURN n
    """
    return run_query(query, {"id": id})