from fastapi import APIRouter
from app.models.schema import ChallengeListResponse, DependencyResponse, DependencyGraphResponse, NeighborsResponse, SubgraphListResponse
from app.service.neo4j_client import run_query

router = APIRouter()

#Challenges als Listenansicht
@router.get("/challenges", tags=["Graph-Info"])
def get_all_challenges() -> list[ChallengeListResponse]:
    query = """
    MATCH (c:Challenge) 
    RETURN c.uuid AS UUID, c.title AS TITLE, c.keywords AS KEYWORDS, c.author AS AUTHOR, c.firstused AS FIRST USED
    """
    return run_query(query)

#Abhängige Challenges als Liste
@router.get("/challenges/{id}/depends-on", tags=["Graph-Info"])
def get_challenge_dependencies(id: str) -> list[DependencyResponse]:
    query = """
    MATCH (c:Challenge {uuid: $id})-[:BUILDS_ON*]->(dep:Challenge)
    RETURN DISTINCT dep.uuid AS UUID, dep.title AS TITLE, dep.keywords AS KEYWORDS
    """
    return run_query(query, {"id": id})

#Challenge Sub-Path als Liste
@router.get("/subgraph/list", tags=["Graph-Info"])
def get_subgraph_list(start: str, end: str) -> list[SubgraphListResponse]:
    query = """
    MATCH path = shortestPath(
        (a:Challenge {uuid: $start})-[:BUILDS_ON*]-(b:Challenge {uuid: $end})
    )
    UNWIND nodes(path) AS node
    RETURN DISTINCT
        node.uuid AS uuid,
        node.title AS title,
        node.keywords AS keywords
    """
    return run_query(query, {"start": start, "end": end})

#Abhängige Challenges als Graph
@router.get("/challenges/{id}/depends-on/graph", tags=["Graph-Info"])
def get_challenge_dependencies_graph(id: str) -> DependencyGraphResponse:
    node_query = """
    MATCH (c:Challenge {uuid: $id})-[:BUILDS_ON*]->(dep:Challenge)
    RETURN DISTINCT dep.uuid AS UUID, dep.title AS TITLE
    """

    edge_query = """
    MATCH (c:Challenge {uuid: $id})-[:BUILDS_ON*]->(a:Challenge)
    MATCH (a)-[:BUILDS_ON]->(b:Challenge)
    RETURN DISTINCT a.uuid AS SOURCE, b.uuid AS TARGET
    """

    nodes = run_query(node_query, {"id": id})
    edges = run_query(edge_query, {"id": id})

    return {
        "nodes": nodes, "edges": edges
    }

#Neighbor Challenges for Pop-Up-Info
@router.get("/challenges/{id}/neighbors", tags=["Challenges"])
def get_challenge_neighbors(id: str) -> NeighborsResponse:
    previous_query = """
    MATCH (prev:Challenge)-[:BUILDS_ON]->(c:Challenge {uuid: $id})
    RETURN prev.uuid AS UUID, prev.title AS TITLE, prev.keywords AS KEYWORDS
    ORDER BY prev.title
    """

    next_query = """
    MATCH (c:Challenge {uuid: $id})-[:BUILDS_ON]->(next:Challenge)
    RETURN next.uuid AS UUID, next.title AS TITLE, next.keywords AS KEYWORDS
    ORDER BY next.title
    """

    previous = run_query(previous_query, {"id": id})
    next_items = run_query(next_query, {"id": id})

    return {
        "previous": previous,
        "next": next_items
    }

