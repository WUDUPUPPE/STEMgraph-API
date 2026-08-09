from typing import Any
from pydantic import BaseModel, Field

#Status Model
class UpdateStatusResponse(BaseModel):
    status: str
    message: str | None = None
    fetch_stats: dict[str, Any] | None = None
    export_stats: dict[str, Any] | None = None

#Read Schedule Model
class ScheduleResponse(BaseModel):
    enabled: bool
    interval_minutes: int

#Update Schedule Model
class ScheduleRequest(BaseModel):
    enabled: bool
    interval_minutes: int = Field(ge=60, le=10080,)

class ScheduleUpdateResponse(BaseModel):
    status: str
    message: str
    schedule: ScheduleResponse

#Manually Update Schedule Model
class ManuallyStartResponse(BaseModel):
    status: str
    message: str