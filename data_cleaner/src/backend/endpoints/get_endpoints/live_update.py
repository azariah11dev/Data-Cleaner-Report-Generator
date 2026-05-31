from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from pathlib import Path
import pandas as pd
import math

live_update_router = APIRouter(prefix="/live-update", tags=["live-update"])


# ---------------------------
# Dependency: upload directory
# ---------------------------
def get_upload_dir() -> Path:
    return (
        Path(__file__)
        .resolve()
        .parent.parent.parent  # go from get_endpoints/live_update.py → backend/
        / "models"
        / "upload_csv"
    )


# ---------------------------
# Helper: make a dict JSON-safe (replace NaN/Inf with None)
# ---------------------------
def make_json_safe(records: list[dict]) -> list[dict]:
    safe = []
    for row in records:
        safe_row = {}
        for k, v in row.items():
            if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
                safe_row[k] = None
            else:
                safe_row[k] = v
        safe.append(safe_row)
    return safe


# ---------------------------
# Preview Endpoint
# ---------------------------
@live_update_router.get("/preview")
async def preview_file(
    file_name: str,
    upload_dir: Path = Depends(get_upload_dir)
):
    file_path = upload_dir / file_name

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Original file not found at {file_path}"
        )

    try:
        df = pd.read_csv(file_path)
        raw_preview = df.head(20).to_dict(orient="records")

        # Replace NaN/Inf so FastAPI can serialize to JSON
        preview = make_json_safe(raw_preview)

        return {
            "columns": df.columns.tolist(),
            "total_rows": len(df),
            "preview": preview
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------
# Download Endpoint
# ---------------------------
@live_update_router.get("/download")
async def download_file(file_path: str):
    path = Path(file_path)

    if not path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"File not found at {path}"
        )

    return FileResponse(
        path=path,
        media_type="text/csv",
        filename=path.name
    )