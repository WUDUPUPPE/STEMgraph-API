from fastapi import APIRouter
from app.models.schema_graph import SubgraphGraphResponse, DependencyGraphResponse, GraphResponse, NeighborsResponse
from app.service.neo4j_client import run_query
    
router = APIRouter()

#All Challenges AS Graph
@router.get("/graph", tags=["Graph-Info"])
def get_graph() -> GraphResponse:
    nodes_query = """
    MATCH (c:Challenge)
    RETURN DISTINCT c.id AS id, c.teaches AS teaches, c.keywords AS keywords, c.author AS author, c.firstused AS firstused
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
def get_graph_dependencies(id: str) -> DependencyGraphResponse:
    node_query = """
    MATCH (c:Challenge {id: $id})
    RETURN DISTINCT c.id AS id, c.teaches AS teaches, c.keywords AS keywords
    UNION
    MATCH (c:Challenge {id: $id})-[:BUILDS_ON*]->(dep:Challenge)
    RETURN DISTINCT dep.id AS id, dep.teaches AS teaches, dep.keywords AS keywords
    """

    edge_query = """
    MATCH (c:Challenge {id: $id})-[:DEPENDS_ON*]->(a:Challenge)
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
        (a:Challenge {id: $start})-[:DEPENDS_ON*]-(b:Challenge {id: $end})
    )
    UNWIND nodes(path) AS node
    RETURN DISTINCT node.id AS id, node.teaches AS teaches, node.keywords AS keywords
    """

    edge_query = """
    MATCH path = shortestPath(
        (a:Challenge {id: $start})-[:DEPENDS_ON*]-(b:Challenge {id: $end})
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

#Neighbor Challenges for Pop-Up-Info
@router.get("/challenges/neighbors", tags=["PopUp-Info"])
def get_challenge_neighbors(id: str) -> NeighborsResponse:
    center_query = """
    MATCH (c:Challenge {id: $id})
    RETURN c.id AS id, c.teaches AS teaches, c.keywords AS keywords
    """

    previous_query = """
    MATCH (prev:Challenge)-[:DEPENDS_ON]->(c:Challenge {id: $id})
    RETURN prev.id AS id, prev.teaches AS teaches, prev.keywords AS keywords
    """

    next_query = """
    MATCH (c:Challenge {id: $id})-[:DEPENDS_ON]->(next:Challenge)
    RETURN next.id AS id, next.teaches AS teaches, next.keywords AS keywords
    ORDER BY next.teaches
    """

    center = run_query(center_query, {"id": id})
    previous = run_query(previous_query, {"id": id})
    next_items = run_query(next_query, {"id": id})

    return {
        "previous": previous,
        "next": next_items
    }