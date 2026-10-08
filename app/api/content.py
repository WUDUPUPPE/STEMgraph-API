from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from app.database.content_queries import readme_query, assets_query, asset_content_query
from app.models.schema_content import AssetResponse, ChallengeContentResponse
from app.service.postgres_client import run_query

router = APIRouter()

@router.get("/challenges/{challenge_id}/content", tags=["Challenge-Content"])
def get_challenge_content(challenge_id: str) -> ChallengeContentResponse:
    readme = run_query(readme_query, (challenge_id,), fetch="one")

    if readme is None:
        raise HTTPException(
            status_code=404, detail="README not Found")

    assets = run_query(assets_query, (challenge_id,), fetch="all")

    return ChallengeContentResponse(
        challenge_id=str(readme[0]),
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


@router.get("/challenges/{challenge_id}/assets/{asset_id}", tags=["Challenge-Content"])
def download_asset(challenge_id: str, asset_id: int):
    asset = run_query(asset_content_query, (asset_id, challenge_id), fetch="one")

    if asset is None:
        raise HTTPException(
            status_code=404, detail="Asset für diese Challenge nicht gefunden")

    content, file_name, mime_type = asset

    return Response(
        content=bytes(content),
        media_type=mime_type or "application/octet-stream",
        headers={
            "Content-Disposition": f'attachment; filename="{file_name}"'
        },
    )