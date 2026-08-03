from pydantic import BaseModel

class UpdateResponse(BaseModel):
    status: str
    message: str
    fetch_stats: dict | None = None
    export_stats: dict | None = None
    