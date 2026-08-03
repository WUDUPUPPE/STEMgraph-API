from fastapi import APIRouter, Query
from app.models.schema_keywords import KeywordsResponse 
from app.service.neo4j_client import run_query
    
router = APIRouter()

@router.get("/keywords", tags=["Keyword-Info"])
def get_keywords() -> KeywordsResponse:
    query = """
    MATCH (c:Challenge) 
    UNWIND c.keywords AS keyword 
    RETURN DISTINCT keyword
    """
    return run_query(query)

@router.get("/keywords/challenges", tags=["Keyword-Info"])
def get_challenges_by_keyword(kw: str = Query) -> KeywordsResponse:
    query = """
    MATCH (c:Challenge) 
    WHERE $kw IN c.keywords 
    RETURN c
    """
    return run_query(query, {"kw": kw})


