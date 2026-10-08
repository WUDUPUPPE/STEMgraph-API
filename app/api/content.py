from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from app.database.content_queries import readme_query, assets_query, asset_content_query
from app.models.schema_content import AssetResponse, ChallengeContentResponse
from app.service.postgres_client import run_query

router = APIRouter()

#Challenge README + Asset-List
@router.get("/challenges/{id}/content", tags=["Content-Info"])
def get_challenge_content(id: str) -> ChallengeContentResponse:
    readme = run_query(readme_query, (id,), fetch="one")

    if readme is None:
        raise HTTPException(
            status_code=404, detail="README not Found")

    assets = run_query(assets_query, (id,), fetch="all")

    return ChallengeContentResponse(
        id=str(readme[0]),
        content_markdown=readme[1],
        source_path=readme[2],
        source_commit=readme[3],
        imported_at=readme[4],
        assets=[
            AssetResponse(
                id=asset[0],
                file_name=asset[1],
                relative_path=asset[2],
                mime_type=asset[3],
                file_size=asset[4],
            )
            for asset in assets
        ],
    )

#Asset Download
@router.get("/challenges/{id}/assets/{file_name}", tags=["Content-Info"])
def download_asset(id: str, file_name: str):
    asset = run_query(asset_content_query, (id, file_name), fetch="one")

    if asset is None:
        raise HTTPException(
            status_code=404, detail="Asset für diese Challenge nicht gefunden")

    content, name, mime_type = asset

    return Response(
        content=bytes(content),
        media_type=mime_type or "application/octet-stream",
        headers={
            "Content-Disposition": f'attachment; filename="{name}"'
        },
    )