import os
import tempfile
import pandas as pd
from fastapi.testclient import TestClient
from fastapi import FastAPI
from pathlib import Path

from src.backend.endpoints.post_endpoint.cleaner_route import cleaner_router
from src.backend.services.cleaner import SheetCleaner
from src.backend.endpoints.post_endpoint.cleaner_route import get_models_dir


# Build a minimal FastAPI app for testing
app = FastAPI()
app.include_router(cleaner_router)

client = TestClient(app)


def test_upload_file_success(tmp_path):
    # Override models directory for this test
    app.dependency_overrides[get_models_dir] = lambda: tmp_path

    csv_content = b"col1,col2\n1,a\n2,b\n"
    upload_file = ("test.csv", csv_content, "text/csv")

    response = client.post(
        "/cleaner/upload",
        files={"file": upload_file}
    )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()

    assert data["message"] == "File uploaded successfully"
    assert data["file_name"] == "test.csv"

    saved_path = tmp_path / "upload_csv" / "test.csv"
    assert saved_path.exists()


def test_clean_file_success(tmp_path):
    # Override models directory
    app.dependency_overrides[get_models_dir] = lambda: tmp_path

    upload_dir = tmp_path / "upload_csv"
    upload_dir.mkdir()

    csv_path = upload_dir / "orders.csv"
    df = pd.DataFrame({
        "category": ["A", None, "B"],
        "price": [10, 20, None]
    })
    df.to_csv(csv_path, index=False)

    response = client.post(
        "/cleaner/clean",
        json={
            "file_name": "orders.csv",
            "missing_strategy": "constant",
            "columns": ["category"],
            "fill_value": "Unknown"
        }
    )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()

    cleaned_path = Path(data["cleaned_file"])
    assert cleaned_path.exists()

    cleaned_df = pd.read_csv(cleaned_path)
    assert cleaned_df["category"].isna().sum() == 0

    # Delete after test
    cleaned_path.unlink()


def test_clean_file_not_found(tmp_path):
    app.dependency_overrides[get_models_dir] = lambda: tmp_path

    response = client.post(
        "/cleaner/clean",
        json={
            "file_name": "missing.csv",
            "missing_strategy": "constant",
            "columns": ["category"],
            "fill_value": "Unknown"
        }
    )

    app.dependency_overrides.clear()

    assert response.status_code == 404
    assert "File not found" in response.json()["detail"]
