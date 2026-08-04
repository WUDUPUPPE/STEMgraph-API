import os
import subprocess
import json
from pathlib import Path
from pydantic import BaseModel
from app.models.schema_admin import UpdateResponse
from fastapi import APIRouter, Header, HTTPException
from app.service.neo4j_client import run_query

router = APIRouter()
WRITE_TOKEN = os.getenv("WRITE_TOKEN")

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