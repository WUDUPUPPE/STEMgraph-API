from pydantic import BaseModel, Field

#Update Response Model
class UpdateResponse(BaseModel):
    status: str
    message: str
    fetch_stats: dict | None = None
    export_stats: dict | None = None


class ScheduleRequest(BaseModel):
    enabled: bool
    interval_minutes: int = Field(ge=60, le=10080,)