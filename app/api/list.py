from fastapi import APIRouter
from app.models.schema_list import ChallengeListResponse, DependencyResponse, DependencyGraphResponse, NeighborsResponse, SubgraphListResponse
from app.service.neo4j_client import run_query

router = APIRouter()

#Challenges als Listenansicht
@router.get("/list", tags=["List-Info"])
def get_list() -> list[ChallengeListResponse]:
    query = """
    MATCH (c:Challenge) 
    RETURN c.uuid AS uuid, c.title AS title, c.keywords AS keywords, c.author AS author, c.firstused AS firstused
    """
    return run_query(query)

#Abhängige Challenges als Liste
@router.get("/list/challenges/{id}/depends-on", tags=["List-Info"])
def get_list_dependencies(id: str) -> list[DependencyResponse]:
    query = """
    MATCH (c:Challenge {uuid: $id})-[:BUILDS_ON*]->(dep:Challenge)
    RETURN DISTINCT dep.uuid AS uuid, dep.title AS title, dep.keywords AS keywords
    """
    return run_query(query, {"id": id})

#Challenge Sub-Path als Liste
@router.get("/sublist", tags=["List-Info"])
def get_sublist(start: str, end: str) -> list[SubgraphListResponse]:
    query = """
    MATCH path = shortestPath(
        (a:Challenge {uuid: $start})-[:BUILDS_ON*]-(b:Challenge {uuid: $end})
    )
    UNWIND nodes(path) AS node
    RETURN DISTINCT node.uuid AS uuid, node.title AS title, node.keywords AS keywords
    """
    return run_query(query, {"start": start, "end": end})

#Neighbor Challenges for Pop-Up-Info
@router.get("/challenges/{id}/neighbors", tags=["PopUp-Info"])
def get_challenge_neighbors(id: str) -> NeighborsResponse:
    previous_query = """
    MATCH (prev:Challenge)-[:BUILDS_ON]->(c:Challenge {uuid: $id})
    RETURN prev.uuid AS uuid, prev.title AS title, prev.keywords AS keywords
    ORDER BY prev.title
    """

    next_query = """
    MATCH (c:Challenge {uuid: $id})-[:BUILDS_ON]->(next:Challenge)
    RETURN next.uuid AS uuid, next.title AS title, next.keywords AS keywords
    ORDER BY next.title
    """

    previous = run_query(previous_query, {"id": id})
    next_items = run_query(next_query, {"id": id})

    return {
        "previous": previous,
        "next": next_items
    }

