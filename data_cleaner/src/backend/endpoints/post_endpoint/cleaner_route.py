from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from pathlib import Path
import pandas as pd

from services.cleaner import SheetCleaner
from schema.schema import CleaningRequest, Stats

cleaner_router = APIRouter(prefix="/cleaner", tags=["cleaner"])

# ---------------------------------------------------------
# Dependency: base models directory
# ---------------------------------------------------------
def get_models_dir() -> Path:
    return (
        Path(__file__)
        .resolve()
        .parent.parent.parent  # go from endpoints/ → backend/
        / "models"
    )


# ---------------------------------------------------------
# Helper: Save uploaded file to correct directory
# ---------------------------------------------------------
def save_uploaded_file(uploaded_file: UploadFile, models_dir: Path) -> Path:
    file_ext = Path(uploaded_file.filename).suffix.lower()

    if file_ext == ".csv":
        folder = "upload_csv"
    elif file_ext in [".xlsx", ".xls"]:
        folder = "upload_excel"
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    save_dir = models_dir / folder
    save_dir.mkdir(parents=True, exist_ok=True)

    file_path = save_dir / uploaded_file.filename

    with open(file_path, "wb") as f:
        f.write(uploaded_file.file.read())

    return file_path


# ---------------------------------------------------------
# Upload
# ---------------------------------------------------------
@cleaner_router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    models_dir: Path = Depends(get_models_dir)
):
    try:
        saved_path = save_uploaded_file(file, models_dir)
        return {
            "message": "File uploaded successfully",
            "file_path": str(saved_path),
            "file_name": file.filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------
# Clean file
# ---------------------------------------------------------
@cleaner_router.post("/clean")
async def clean_file(
    data: CleaningRequest,
    models_dir: Path = Depends(get_models_dir)
):
    try:
        upload_path = models_dir / "upload_csv" / data.file_name
        cleaned_path = models_dir / "save_csv" / data.file_name

        # Use cleaned file if it exists
        file_to_clean = cleaned_path if cleaned_path.exists() else upload_path

        if not file_to_clean.exists():
            raise HTTPException(
                status_code=404,
                detail=f"File not found at {file_to_clean}"
            )

        cleaner = SheetCleaner(
            file_name=data.file_name,
            file_path=str(file_to_clean)
        )

        stats = cleaner.run(
            missing_strategy=data.missing_strategy,
            columns=data.columns,
            fill_value=data.fill_value
        )

        new_cleaned_path = cleaner.save_cleaned_data()

        return {
            "message": "File cleaned successfully",
            "original_file": str(file_to_clean),
            "cleaned_file": str(new_cleaned_path),
            "stats": Stats(**stats).model_dump()
        }
    
    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
