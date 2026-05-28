from fastapi import APIRouter, HTTPException
import os

delete_file_router = APIRouter(prefix="/delete", tags=["delete"])


@delete_file_router.delete("/{filename}")
async def delete_file(filename: str):
    try:
        # Determine file extension
        ext = os.path.splitext(filename)[1].lower()

        # Resolve backend root
        base_dir = os.path.dirname(os.path.abspath(__file__))
        endpoints_dir = os.path.dirname(base_dir)
        backend_dir = os.path.dirname(endpoints_dir)

        # Determine upload + save directories
        if ext == ".csv":
            upload_dir = os.path.join(backend_dir, "models", "upload_csv")
            save_dir = os.path.join(backend_dir, "models", "save_csv")
        elif ext in [".xlsx", ".xls"]:
            upload_dir = os.path.join(backend_dir, "models", "upload_excel")
            save_dir = os.path.join(backend_dir, "models", "save_excel")
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        # Full paths
        upload_path = os.path.join(upload_dir, filename)

        # Cleaned file is always saved as CSV
        cleaned_name = (
            filename.replace(".xlsx", ".csv")
                    .replace(".xls", ".csv")
        )
        cleaned_path = os.path.join(save_dir, cleaned_name)

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
