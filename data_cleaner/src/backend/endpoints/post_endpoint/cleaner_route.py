from fastapi import APIRouter, HTTPException, UploadFile, File
import os
from typing import Any

from services.cleaner import SheetCleaner

cleaner_router = APIRouter(prefix="/cleaner", tags=["cleaner"])

# ---------------------------------------------------------
# Helper: Save uploaded file to correct directory
# ---------------------------------------------------------
def save_uploaded_file(uploaded_file: UploadFile):
    file_ext = os.path.splitext(uploaded_file.filename)[1].lower()

    # Decide folder based on extension
    if file_ext == ".csv":
        folder = "upload_csv"
    elif file_ext in [".xlsx", ".xls"]:
        folder = "upload_excel"
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    endpoints_dir = os.path.dirname(base_dir)
    backend_dir = os.path.dirname(endpoints_dir)
    save_dir = os.path.join(backend_dir, "models", folder)
    os.makedirs(save_dir, exist_ok=True)

    file_path = os.path.join(save_dir, uploaded_file.filename)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.file.read())

    return file_path


# ---------------------------------------------------------
# Upload + Clean Endpoint
# ---------------------------------------------------------
@cleaner_router.post("/upload")
async def upload_file(fill_value: Any,
                      columns: list,
                      missing_strategy: str,
                      file: UploadFile = File(...)):
    try:
        # Save file to correct folder
        saved_path = save_uploaded_file(file)

        # Run cleaner
        cleaner = SheetCleaner(
            file_name=file.filename,
            file_path=saved_path
        )
        stats = cleaner.run(missing_strategy=missing_strategy,
                            columns=columns,
                            fill_value=fill_value)
        cleaned_path = cleaner.save_cleaned_data()

        return {
            "message": "File uploaded and cleaned successfully",
            "original_file": saved_path,
            "cleaned_file": cleaned_path,
            "stats": stats
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
