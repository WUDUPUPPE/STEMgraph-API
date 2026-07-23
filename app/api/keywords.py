from fastapi import APIRouter
from app.service.neo4j_client import run_query

router = APIRouter()

@router.get("/keywords", tags=["Graph-Info"])
def get_keywords():
    query = "MATCH (c:Challenge) UNWIND c.keywords AS keyword RETURN DISTINCT keyword"
    return run_query(query)

@router.get("/keywords/{kw}/challenges", tags=["Graph-Info"])
def get_challenges_by_keyword(kw: str):
    query = "MATCH (c:Challenge) WHERE $kw IN c.keywords RETURN c"
    return run_query(query, {"kw": kw})


