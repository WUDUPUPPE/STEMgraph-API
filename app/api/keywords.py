from fastapi import APIRouter, Query
from app.models.schema_keywords import KeywordListResponse, ChallengesByKeywordListResponse, ChallengeByKeywordListItem,KeywordGraphResponse, KeywordNode, KeywordEdge, ChallengesByKeywordGraphResponse, ChallengeNode, ChallengeEdge
from app.service.neo4j_client import run_query
    
router = APIRouter()

#Keywords AS List
@router.get("/keywords/list", tags=["Keyword-Info"])
def get_keywords_list() -> KeywordListResponse:
    query = """
    MATCH (c:Challenge)
    UNWIND c.keywords AS keyword
    RETURN DISTINCT keywords AS keyword
    """
    rows = run_query(query)
    return KeywordListResponse(
        keywords=[row["keyword"] for row in rows]
    )

#Challenges by Keyword AS List
@router.get("/keywords/challenges/list", tags=["Keyword-Info"])
def get_challenges_by_keyword_list(kw: str = Query()) -> ChallengesByKeywordListResponse:
    query = """
    MATCH (c:Challenge)
    WHERE $kw IN c.keywords
    RETURN c.id AS id, c.teaches AS title, c.keywords AS keyword
    """
    rows = run_query(query, {"kw": kw})
    items = [ChallengeByKeywordListItem(**row) for row in rows]
    return ChallengesByKeywordListResponse(items=items)

#Keywords AS Graph
@router.get("/keywords/graph", tags=["Keyword-Info"])
def get_keyword_graph() -> KeywordGraphResponse:
    query = """
    MATCH (c:Challenge)
    UNWIND c.keywords AS keyword
    RETURN DISTINCT keywords AS keyword, c.id AS id
    """
    rows = run_query(query)

    keywords_seen = set()
    nodes: list[KeywordNode] = []
    edges: list[KeywordEdge] = []

    for row in rows:
        kw = row["keyword"]
        id = row["id"]
        if kw not in keywords_seen:
            nodes.append(KeywordNode(keyword=kw))
            keywords_seen.add(kw)
        edges.append(KeywordEdge(keyword=kw, challenge_id=id))

    return KeywordGraphResponse(nodes=nodes, edges=edges)

#Challenges by Keyword AS Graph
@router.get("/keywords/challenges/graph", tags=["Keyword-Info"])
def get_challenges_by_keyword_graph(kw: str = Query()) -> ChallengesByKeywordGraphResponse:
    node_query = """
    MATCH (c:Challenge)
    WHERE $kw IN c.keywords
    RETURN DISTINCT c.id AS id, c.teaches AS title, c.keywords AS keywords
    """

    edge_query = """
    MATCH (a:Challenge)-[:DEPENDS_ON]->(b:Challenge)
    WHERE $kw IN a.keywords AND $kw IN b.keywords
    RETURN DISTINCT a.id AS source, b.id AS target
    """

    params = {"kw": kw}

    nodes_rows = run_query(node_query, params)
    edges_rows = run_query(edge_query, params)

    nodes = [ChallengeNode(**row) for row in nodes_rows]
    edges = [ChallengeEdge(**row) for row in edges_rows]

    return ChallengesByKeywordGraphResponse(nodes=nodes, edges=edges)