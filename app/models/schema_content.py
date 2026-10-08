from datetime import datetime
from pydantic import BaseModel


class AssetResponse(BaseModel):
    id: int
    file_name: str
    relative_path: str
    mime_type: str | None
    file_size: int


class ChallengeContentResponse(BaseModel):
    id: str
    content_markdown: str
    source_path: str
    source_commit: str | None
    imported_at: datetime
    assets: list[AssetResponse]