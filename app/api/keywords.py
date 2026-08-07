from fastapi import APIRouter, Query
from app.models.schema_keywords import KeywordListResponse, ChallengesByKeywordListResponse, ChallengeByKeywordListItem,KeywordGraphResponse, KeywordNode, KeywordEdge, ChallengesByKeywordGraphResponse, ChallengeNode, ChallengeEdge
from app.database.keyword_queries import key_list_query, chal_by_key_list_query, key_graph_query, chal_by_key_graph_node_query, chal_by_key_graph_edge_query
from app.service.neo4j_client import run_query
    
router = APIRouter()

#Keywords AS List
@router.get("/keywords/list", tags=["Keyword-Info"])
def get_keywords_list() -> KeywordListResponse:

    rows = run_query(key_list_query)
    
    return KeywordListResponse(
        keywords=[row["keywords"] for row in rows]
    )

#Challenges by Keyword AS List
@router.get("/keywords/challenges/list", tags=["Keyword-Info"])
def get_challenges_by_keyword_list(kw: str = Query()) -> ChallengesByKeywordListResponse:

    rows = run_query(chal_by_key_list_query, {"kw": kw})
    items = [ChallengeByKeywordListItem(**row) for row in rows]
    
    return ChallengesByKeywordListResponse(
        items=items
        )

#Keywords AS Graph
@router.get("/keywords/graph", tags=["Keyword-Info"])
def get_keywords_graph() -> KeywordGraphResponse:

    rows = run_query(key_graph_query)

    keywords_seen = set()
    nodes: list[KeywordNode] = []
    edges: list[KeywordEdge] = []

    for row in rows:
        id = row["id"]
        kw = row["keywords"]
        if kw not in keywords_seen:
            nodes.append(KeywordNode(keywords=kw))
            keywords_seen.add(kw)
        edges.append(KeywordEdge(id=id), keywords=kw)

    return KeywordGraphResponse(
        nodes=nodes, edges=edges
        )

#Challenges by Keyword AS Graph
@router.get("/keywords/challenges/graph", tags=["Keyword-Info"])
def get_challenges_by_keyword_graph(kw: str = Query()) -> ChallengesByKeywordGraphResponse:

    params = {"kw": kw}

    nodes_rows = run_query(chal_by_key_graph_node_query, params)
    edges_rows = run_query(chal_by_key_graph_edge_query, params)

    nodes = [ChallengeNode(**row) for row in nodes_rows]
    edges = [ChallengeEdge(**row) for row in edges_rows]

    return ChallengesByKeywordGraphResponse(
        nodes=nodes, edges=edges
        )