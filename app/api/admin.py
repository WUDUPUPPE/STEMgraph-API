import os
import subprocess
import json
import asyncio
from pathlib import Path
from pydantic import BaseModel
from fastapi import APIRouter, Header, HTTPException, BackgroundTasks
from app.models.schema_admin import UpdateResponse, ScheduleRequest
from app.service.task_scheduler import execute_update, last_update_status, schedule_changed, schedule_config

router = APIRouter()
WRITE_TOKEN = os.getenv("WRITE_TOKEN")

def check_api_key(x_api_key: str) -> None:
    if x_api_key != WRITE_TOKEN:
        raise HTTPException(status_code=403,detail="Invalid API Key",)

#Manuel Update
@router.post("/admin/update-challenges", tags=["Admin/Health Check"])
async def admin_update_challenges(background_tasks: BackgroundTasks, x_api_key: str = Header(...)):
    check_api_key
    if last_update_status["status"] == "running":
        return {"status": "already_running", "message": ("An update is already running")
        }

    background_tasks.add_task(execute_update,)

    return {"status": "started","message": ("Challenge update started")
    }

#Status
@router.get("/admin/update-status", tags=["Admin/Health Check"])
def get_update_status(x_api_key: str = Header(...)): 
    check_api_key(x_api_key)
    
    return last_update_status

#Read Schedule
@router.get("/admin/schedule",tags=["Admin/Health Check"])
def get_schedule(x_api_key: str = Header(...)):
    check_api_key(x_api_key)

    return schedule_config

@router.put("/admin/schedule",tags=["Admin/Health Check"])
def update_schedule(schedule: ScheduleRequest, x_api_key: str = Header(...)):
    check_api_key(x_api_key)

    schedule_config["enabled"] = schedule.enabled
    schedule_config["interval_minutes"] = (schedule.interval_minutes    )

    schedule_changed.set()
    
    return {"status": "ok", "message": "Schedule updated", "schedule": schedule_config,
    }






@router.post("/admin/update-challenges", tags=["Admin/Health Check"])
def admin_update_challenges(x_api_key: str = Header(...)) -> UpdateResponse:
    if x_api_key != WRITE_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid API Key")

    # 1. Shell-Skripte ausführen (Reihenfolge: get_all → export → load_neo4j)
    try:
        subprocess.run(
            ["bash", "app/scripts/get_all_challenges.sh"],
            check=True,
        )
        subprocess.run(
            ["bash", "app/scripts/export_graph_data.sh"],
            check=True,
        )
        subprocess.run(
            ["bash", "app/scripts/load_neo4j.sh"],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Update process failed: {e}",
        )

    # 2. Stats-Dateien einlesen
    fetch_stats_path = Path("../data/stats_fetch.json")
    export_stats_path = Path("../data/stats_export.json")

    fetch_stats: dict | None = None
    export_stats: dict | None = None

    if fetch_stats_path.is_file():
        try:
            fetch_stats = json.loads(
                fetch_stats_path.read_text(encoding="utf-8")
            )
        except Exception:
            fetch_stats = None

    if export_stats_path.is_file():
        try:
            export_stats = json.loads(
                export_stats_path.read_text(encoding="utf-8")
            )
        except Exception:
            export_stats = None

    return UpdateResponse(
        status="ok", message="Challenges updated, graph exported and Neo4j loaded",
        fetch_stats=fetch_stats, export_stats=export_stats,
    )