import os
from fastapi import APIRouter, Header, HTTPException
from app.service.neo4j_client import run_query

router = APIRouter()
WRITE_TOKEN = os.getenv("WRITE_TOKEN")

@router.post("/admin/update-challenges", tags=["Admin"])
def update_challenges(x_api_key: str = Header(...)):
    if x_api_key != WRITE_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return {"status": "ok", "message": "Challenges updated"}