from fastapi import APIRouter, HTTPException
import pandas as pd
import os

live_update_router = APIRouter(prefix="/live-update", tags=["live-update"])

@live_update_router.get("/changes")
async def get_changes(cleaned_file_path: str, preview_rows: int = 20):
    try:
        if not os.path.exists(cleaned_file_path):
            raise HTTPException(status_code=404, detail="Cleaned file not found")

        df = pd.read_csv(cleaned_file_path)

        preview = df.head(preview_rows).to_dict(orient="records")

        return {
            "columns": df.columns.tolist(),
            "total_rows": len(df),
            "preview": preview
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
