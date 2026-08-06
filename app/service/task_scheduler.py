import asyncio
import json
import subprocess
from pathlib import Path

from app.models.schema_admin import UpdateResponse

last_update_status: dict = {
    "status": "not_started", "message": None, 
    "fetch_stats": None, 
    "export_stats": None,
}

schedule_config: dict = {
    "enabled": False, "interval_minutes": 1440,
}

schedule_changed = asyncio.Event()
update_lock = asyncio.Lock()

# Update-Pipeline
def run_update_process() -> UpdateResponse:
    global last_update_status

    last_update_status = {
        "status": "running", "message": "Update process is running", 
        "fetch_stats": None, 
        "export_stats": None,
    }
    try:
        subprocess.run(["bash", "app/scripts/get_all_challenges.sh"], check=True)
        subprocess.run(["bash", "app/scripts/export_graph_data.sh"], check=True)
        subprocess.run(["bash", "app/scripts/load_neo4j.sh"], check=True)

    except subprocess.CalledProcessError as error:
        last_update_status = {
            "status": "failed", "message": f"Update process failed: {error}", 
            "fetch_stats": None, 
            "export_stats": None,
        }

        raise error

    fetch_stats_path = Path("../data/stats_fetch.json")
    export_stats_path = Path("../data/stats_export.json")

    fetch_stats: dict | None = None
    export_stats: dict | None = None

    if fetch_stats_path.is_file():
        try:
            fetch_stats = json.loads(fetch_stats_path.read_text(encoding="utf-8"))
        except Exception:
            fetch_stats = None

    if export_stats_path.is_file():
        try:
            export_stats = json.loads(export_stats_path.read_text(encoding="utf-8",))
        except Exception:
            export_stats = None

    last_update_status = {
        "status": "ok", "message": ("Challenges updated, graph exported and Neo4j loaded"),
        "fetch_stats": fetch_stats,
        "export_stats": export_stats,
    }

    return UpdateResponse(
        status="ok", message=("Challenges updated, graph exported and Neo4j loaded"),
        fetch_stats=fetch_stats,
        export_stats=export_stats,
    )

# Update im Hintergrund
async def execute_update() -> None:
    try:
        async with update_lock:
            await asyncio.to_thread(run_update_process)

    except Exception as error:
        print(f"Challenge update failed: {error}")

# Automatischer Scheduler
async def scheduler_loop(
    stop_event: asyncio.Event,
):
    while not stop_event.is_set():

        if schedule_config["enabled"]:
            print("Automatic challenge update started")

            await execute_update()

            print("Automatic challenge update finished")

            interval_seconds = (schedule_config["interval_minutes"]* 60)

        else:
            interval_seconds = 60

        try:
            await asyncio.wait_for(schedule_changed.wait(), timeout=interval_seconds)

            schedule_changed.clear()

        except asyncio.TimeoutError:
            pass

# Lifespan-Hilfsfunktionen
def create_stop_event() -> asyncio.Event:
    return asyncio.Event()

async def start_scheduler(
    stop_event: asyncio.Event,
):
    return asyncio.create_task(
        scheduler_loop(stop_event),
)

async def stop_scheduler(
    stop_event: asyncio.Event,
    scheduler_task: asyncio.Task,
):
    stop_event.set()
    schedule_changed.set()
    await scheduler_task