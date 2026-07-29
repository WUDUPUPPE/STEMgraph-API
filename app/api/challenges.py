from fastapi import APIRouter
from pydantic import BaseModel
from app.service.neo4j_client import run_query

class ChallengesResponse(BaseModel):
    uuid: str
    title: str | None = None
    keywords: list[str] = []

router = APIRouter()

@router.get("/challenges", tags=["Graph-Info"])
def get_all_challenges() -> list[ChallengesResponse]:
    query = "MATCH (c:Challenge) RETURN c"
    return run_query(query)

@router.get("/challenges/{id}/depends-on", tags=["Graph-Info"])
def get_challenge_dependencies(id: str, format: str ="list") -> list[str]:
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

@router.get("/challenges/{id}/neighbors", tags=["Graph-Info"])
def get_challenge_neighbors(id: str) -> dict[str, str]:
    query = """
    MATCH (c:Challenge {uuid:$id})-[:BUILDS_ON]-(n)
    RETURN n
    """
    return run_query(query, {"id": id})