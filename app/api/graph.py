from fastapi import APIRouter
from app.models.schema import SubgraphGraphResponse, DependencyGraphResponse, GraphResponse
from app.service.neo4j_client import run_query
    
router = APIRouter()

#All Challenges AS Graph
@router.get("/graph", tags=["Graph-Info"])
def get_graph() -> GraphResponse:
    nodes_query = """
    MATCH (c:Challenge)
    RETURN DISTINCT c.uuid AS uuid, c.title AS title
    """

    edges_query = """
    MATCH (c:Challenge)-[:BUILDS_ON]->(dep:Challenge)
    RETURN DISTINCT c.uuid AS source, dep.uuid AS target
    """

    return {
        "nodes": run_query(nodes_query),
        "edges": run_query(edges_query),
    }

#Dependency Challenges AS Graph
@router.get("/graph/challenges/{id}/depends-on", tags=["Graph-Info"])
def get_graph_dependencies(id: str) -> DependencyGraphResponse:
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

#Subgraph Path AS Graph
@router.get("/subgraph", tags=["Graph-Info"])
def get_subGraph(start: str, end: str) -> SubgraphGraphResponse:
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