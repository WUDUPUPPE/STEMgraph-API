import os
from fastapi import APIRouter, Header, HTTPException
from app.service.neo4j_client import run_query

router = APIRouter()
WRITE_TOKEN = os.getenv("WRITE_TOKEN")

@router.post("/admin/update-challenges")
def update_challenges(x_api_key: str = Header(...)):
    if x_api_key != WRITE_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return {"status": "ok", "message": "Challenges updated"}

@router.post("/admin/load-authors")
def load_authors(x_api_key: str = Header(...)):
    if x_api_key != WRITE_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    query = """
    MATCH (c:Challenge {uuid: $uuid})
    SET c.author = $author, c.author_email = $author_email
    """
    run_query(query, {"uuid": uuid, "author": author, "author_email": author_email})
    return {"status": "authors loaded"}