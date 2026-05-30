import os
import tempfile
import pandas as pd
from fastapi.testclient import TestClient
from fastapi import FastAPI
from pathlib import Path

from src.backend.endpoints.get_endpoints.live_update import live_update_router
from src.backend.endpoints.get_endpoints.live_update import get_upload_dir


# Build a minimal FastAPI app for testing
app = FastAPI()
app.include_router(live_update_router)

client = TestClient(app)


def test_preview_file_success(tmp_path):
    """
    Test that /live-update/preview returns correct structure
    when a valid CSV exists in models/upload_csv.
    """

    # Create folder structure: backend/models/upload_csv/
    upload_dir = tmp_path
    upload_dir.mkdir(exist_ok=True)

    # Create a temporary CSV file
    csv_path = upload_dir / "test.csv"
    df = pd.DataFrame({
        "col1": [1, 2, 3],
        "col2": ["a", "b", "c"]
    })
    df.to_csv(csv_path, index=False)

    # Override dependency so endpoint uses tmp_path
    app.dependency_overrides[get_upload_dir] = lambda: upload_dir

    try:
        response = client.get("/live-update/preview", params={"file_name": "test.csv"})
    except Exception as e:
        raise FileNotFoundError(f"Error during test: {e}")

    assert response.status_code == 200
    data = response.json()

    assert "columns" in data
    assert "total_rows" in data
    assert "preview" in data

    assert data["columns"] == ["col1", "col2"]
    assert data["total_rows"] == 3
    assert len(data["preview"]) == 3

    # Clean override
    app.dependency_overrides.clear()


def test_preview_file_not_found(tmp_path):
    """
    Test that preview returns 404 when file does not exist.
    """

    cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        response = client.get("/live-update/preview", params={"file_name": "missing.csv"})
    finally:
        os.chdir(cwd)

    assert response.status_code == 404
    assert "Original file not found" in response.json()["detail"]


def test_download_file_success(tmp_path):
    """
    Test that /live-update/download returns a FileResponse
    when the file exists.
    """

    # Create a temporary CSV file
    csv_path = tmp_path / "cleaned.csv"
    csv_path.write_text("col1,col2\n1,a\n2,b\n")

    response = client.get(
        "/live-update/download",
        params={"file_path": str(csv_path)}
    )

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")
    assert response.headers["content-disposition"].startswith("attachment")


def test_download_file_not_found():
    """
    Test that download returns 404 when file does not exist.
    """

    response = client.get(
        "/live-update/download",
        params={"file_path": "/tmp/does_not_exist.csv"}
    )

    assert response.status_code == 404
    assert "File not found" in response.json()["detail"]
