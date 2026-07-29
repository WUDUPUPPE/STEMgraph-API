import os
from pydantic import BaseModel
from fastapi import APIRouter, Header, HTTPException
from app.service.neo4j_client import run_query

class UpdateResponse(BaseModel):
    status: str
    message: str
    
router = APIRouter()
WRITE_TOKEN = os.getenv("WRITE_TOKEN")

@router.post("/admin/update-challenges", tags=["Admin/Health Check"])
def update_challenges(x_api_key: str = Header(...)) -> UpdateResponse:
    if x_api_key != WRITE_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return UpdateResponse(
        status="ok", message="Challenges successfully updated and generated JSON"
    )
