from fastapi import APIRouter
from app.models.schema import SubgraphGraphResponse
from app.service.neo4j_client import run_query
    
router = APIRouter()

@router.get("/graph", tags=["Graph-Info"])
def get_graph():
    query = """
    MATCH (c:Challenge)
    OPTIONAL MATCH (c)-[r:BUILDS_ON]->(dep:Challenge)
    RETURN DISTINCT c.uuid AS SOURCE, c.title AS source_TITLE, dep.uuid AS TARGET, dep.title AS target_TITLE
    """
    return run_query(query)

@router.get("/subgraph/graph", tags=["Graph-Info"])
def get_subgraph_graph(start: str, end: str) -> SubgraphGraphResponse:
    node_query = """
    MATCH path = shortestPath(
        (a:Challenge {uuid: $start})-[:BUILDS_ON*]-(b:Challenge {uuid: $end})
    )
    UNWIND nodes(path) AS node
    RETURN DISTINCT node.uuid AS UUID, node.title AS TITLE, node.keywords AS KEYWORDS
    """

    edge_query = """
    MATCH path = shortestPath(
        (a:Challenge {uuid: $start})-[:BUILDS_ON*]-(b:Challenge {uuid: $end})
    )
    UNWIND relationships(path) AS rel
    RETURN DISTINCT startNode(rel).uuid AS SOURCE, endNode(rel).uuid AS TARGET
    """

    nodes = run_query(node_query, {"start": start, "end": end})
    edges = run_query(edge_query, {"start": start, "end": end})

    return {
        "nodes": nodes,
        "edges": edges
    }