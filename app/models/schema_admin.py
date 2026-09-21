from typing import Any
from pydantic import BaseModel, Field

#Update Status Model
class UpdateStatusResponse(BaseModel):
    status: str
    message: str | None = None
    fetch_stats: dict[str, Any] | None = None
    export_stats: dict[str, Any] | None = None

#API & Data Status
class DataApiStatusResponse(BaseModel):
    status: str
    api: str
    database: str
    message: str
    
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