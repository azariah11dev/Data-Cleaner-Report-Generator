from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from pathlib import Path
import pandas as pd

live_update_router = APIRouter(prefix="/live-update", tags=["live-update"])


# ---------------------------
# Dependency: upload directory
# ---------------------------
def get_upload_dir() -> Path:
    # Default directory used by the running app
    return (
        Path(__file__)
        .resolve()
        .parent.parent.parent  # go from get_endpoints/live_update.py → backend/
        / "models"
        / "upload_csv"
    )


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
        preview = df.head(20).to_dict(orient="records")

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
    file_path = Path(file_path)

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"File not found at {file_path}"
        )

    return FileResponse(
        path=file_path,
        media_type="text/csv",
        filename=file_path.name
    )
