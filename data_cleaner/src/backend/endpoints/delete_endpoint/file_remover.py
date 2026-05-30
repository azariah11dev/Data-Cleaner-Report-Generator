from fastapi import APIRouter, HTTPException
import os

delete_file_router = APIRouter(prefix="/delete", tags=["delete"])


@delete_file_router.delete("/target")
async def delete_file(upload_path: str, cleaned_path: str):
    try:
        # Delete uploaded file
        if os.path.exists(upload_path):
            os.remove(upload_path)

        # Delete cleaned file
        if os.path.exists(cleaned_path):
            os.remove(cleaned_path)

        return {
            "message": "File(s) deleted successfully",
            "deleted_upload": upload_path,
            "deleted_cleaned": cleaned_path
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
