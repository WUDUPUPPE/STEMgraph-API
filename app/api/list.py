from fastapi import APIRouter
from app.models.schema_list import ChallengeListResponse, DependencyResponse, SubgraphListResponse
from app.service.neo4j_client import run_query

router = APIRouter()

#All Challenges AS List
@router.get("/list", tags=["List-Info"])
def get_list() -> list[ChallengeListResponse]:
    query = """
    MATCH (c:Challenge) 
    RETURN c.id AS id, c.teaches AS teaches, c.keywords AS keywords, c.author AS author, c.firstused AS firstused
    """
    return run_query(query)

#Dependency Challenges AS List
@router.get("/list/challenges/depends-on", tags=["List-Info"])
def get_list_dependencies(id: str) -> list[DependencyResponse]:
    query = """
    MATCH (c:Challenge)-[:DEPENDS_ON*]->(dep:Challenge)
    RETURN DISTINCT dep.id AS id, dep.teaches AS teaches, dep.keywords AS keywords
    """
    return run_query(query)

#Subgraph Path AS List
@router.get("/sublist", tags=["List-Info"])
def get_sublist(start: str, end: str) -> list[SubgraphListResponse]:
    query = """
    MATCH path = shortestPath(
        (a:Challenge {id: $start})-[:DEPENDS_ON*]-(b:Challenge {id: $end})
    )
    UNWIND nodes(path) AS node
    RETURN DISTINCT node.id AS id, node.teaches AS teaches, node.keywords AS keywords
    """
    return run_query(query, {"start": start, "end": end})
