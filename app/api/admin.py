import os
from fastapi import APIRouter, Header, HTTPException, BackgroundTasks
from app.models.schema_admin import UpdateStatusResponse, ScheduleResponse, ScheduleRequest, ScheduleUpdateResponse, ManuallyStartResponse
from app.service import task_scheduler

router = APIRouter()
WRITE_TOKEN = os.getenv("WRITE_TOKEN")

def check_api_key(x_api_key: str) -> None:
    if x_api_key != WRITE_TOKEN:
        raise HTTPException(status_code=403,detail="Invalid API Key",)

#Status
@router.get("/admin/update-status", tags=["Admin/Health Check"])
def get_update_status(x_api_key: str = Header(...)) -> UpdateStatusResponse: 
    check_api_key(x_api_key)
    
    return UpdateStatusResponse(task_scheduler.schedule_config
    )
    
#Read Schedule
@router.get("/admin/schedule",tags=["Admin/Health Check"])
def get_schedule(x_api_key: str = Header(...)) -> ScheduleResponse:
    check_api_key(x_api_key)

    return ScheduleResponse(task_scheduler.schedule_config
    )
    
#Update Schedule
@router.put("/admin/schedule",tags=["Admin/Health Check"])
def update_schedule(schedule: ScheduleRequest, x_api_key: str = Header(...)) -> ScheduleUpdateResponse:
    check_api_key(x_api_key)

    task_scheduler.schedule_config["enabled"] = schedule.enabled
    task_scheduler.schedule_config["interval_minutes"] = (schedule.interval_minutes    )

    task_scheduler.schedule_changed.set()
    
    return ScheduleUpdateResponse(
        status= "ok", 
        message = "Schedule updated", 
        schedule = ScheduleUpdateResponse(task_scheduler.schedule_config)
    )

#Manuel Update
@router.post("/admin/update-challenges", tags=["Admin/Health Check"])
async def admin_update_challenges(background_tasks: BackgroundTasks, x_api_key: str = Header(...)) -> ManuallyStartResponse:
    check_api_key(x_api_key)
    if task_scheduler.last_update_status["status"] == "running":
        
        return ManuallyStartResponse(
            status = "already_running", 
            message = "An update is already running",
        )
        
    background_tasks.add_task(task_scheduler.execute_update,)

    return ManuallyStartResponse(
        status = "started",
        message = "Challenge update started",
    )