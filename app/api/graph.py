from fastapi import APIRouter
from app.models.schema_graph import SubgraphGraphResponse, DependencyGraphResponse, GraphResponse
from app.service.neo4j_client import run_query
    
router = APIRouter()

#All Challenges AS Graph
@router.get("/graph", tags=["Graph-Info"])
def get_graph() -> GraphResponse:
    nodes_query = """
    MATCH (c:Challenge)
    RETURN DISTINCT c.id AS uuid, c.teaches AS title
    """

    edges_query = """
    MATCH (c:Challenge)-[:DEPENDS_ON]->(dep:Challenge)
    RETURN DISTINCT c.id AS source, dep.id AS target
    """

    return {
        "nodes": run_query(nodes_query),
        "edges": run_query(edges_query),
    }

#Dependency Challenges AS Graph
@router.get("/graph/challenges/depends-on", tags=["Graph-Info"])
def get_graph_dependencies() -> DependencyGraphResponse:
    node_query = """
    MATCH (c:Challenge)-[:BUILDS_ON*]->(dep:Challenge)
    RETURN DISTINCT dep.id AS uuid, dep.teaches AS title
    """

    edge_query = """
    MATCH (c:Challenge)-[:DEPENDS_ON*]->(a:Challenge)
    MATCH (a)-[:DEPENDS_ON]->(b:Challenge)
    RETURN DISTINCT a.id AS source, b.id AS target
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
        (a:Challenge {uuid: $start})-[:DEPENDS_ON*]-(b:Challenge {uuid: $end})
    )
    UNWIND nodes(path) AS node
    RETURN DISTINCT node.id AS uuid, node.teaches AS title, node.keywords AS keywords
    """

    edge_query = """
    MATCH path = shortestPath(
        (a:Challenge {uuid: $start})-[:DEPENDS_ON*]-(b:Challenge {uuid: $end})
    )
    UNWIND relationships(path) AS rel
    RETURN DISTINCT startNode(rel).id AS source, endNode(rel).id AS target
    """

    nodes = run_query(node_query, {"start": start, "end": end})
    edges = run_query(edge_query, {"start": start, "end": end})

    return {
        "nodes": nodes,
        "edges": edges
    }
    
@router.get("/graph-test", tags=["Graph-Info"])
def graph_test():
    test_query = "MATCH (n) RETURN count(n) AS count"
    return run_query(test_query)