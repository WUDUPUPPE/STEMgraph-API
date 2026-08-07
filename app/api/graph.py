from fastapi import APIRouter
from app.models.schema_graph import GraphResponse, DependencyGraphResponse, SubgraphGraphResponse,  NeighborsResponse
from app.database.graph_queries import all_nodes_query, all_edges_query, dep_node_query, dep_edge_query, sub_node_query, sub_edge_query, center_query, previous_query, next_query
from app.service.neo4j_client import run_query
    
router = APIRouter()

#All Challenges AS Graph
@router.get("/graph", tags=["Graph-Info"])
def get_graph() -> GraphResponse:

    nodes = run_query(all_nodes_query)
    edges = run_query(all_edges_query)
    
    return GraphResponse (
        nodes=nodes, edges=edges
        )

#Dependency Challenges AS Graph
@router.get("/graph/challenges/depends-on", tags=["Graph-Info"])
def get_graph_dependencies(id: str) -> DependencyGraphResponse:

    nodes = run_query(dep_node_query, {"id": id})
    edges = run_query(dep_edge_query, {"id": id})

    return DependencyGraphResponse(
        nodes=nodes, edges=edges
    )

#Subgraph Path AS Graph
@router.get("/subgraph", tags=["Graph-Info"])
def get_subGraph(start: str, end: str) -> SubgraphGraphResponse:

    nodes = run_query(sub_node_query, {"start": start, "end": end})
    edges = run_query(sub_edge_query, {"start": start, "end": end})

    return SubgraphGraphResponse(
        nodes=nodes, edges=edges
    )

#Neighbor Challenges for Pop-Up-Info
@router.get("/challenges/neighbors", tags=["PopUp-Info"])
def get_challenge_neighbors(id: str) -> NeighborsResponse:

    center = run_query(center_query, {"id": id})
    previous = run_query(previous_query, {"id": id})
    next_items = run_query(next_query, {"id": id})

    return NeighborsResponse(
        center=center, previous=previous, next=next_items
    )   