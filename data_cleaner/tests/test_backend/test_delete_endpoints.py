import os
import tempfile
from fastapi.testclient import TestClient
from fastapi import FastAPI

from src.backend.endpoints.delete_endpoint import delete_file_router

# Build a minimal FastAPI app for testing
app = FastAPI()
app.include_router(delete_file_router)

client = TestClient(app)


def test_delete_files_success():
    # Create two temporary files to simulate upload + cleaned files
    upload_fd, upload_path = tempfile.mkstemp()
    cleaned_fd, cleaned_path = tempfile.mkstemp()

    # Close file descriptors (we only need the paths)
    os.close(upload_fd)
    os.close(cleaned_fd)

    # Ensure files exist before deletion
    assert os.path.exists(upload_path)
    assert os.path.exists(cleaned_path)

    # Call the delete endpoint
    response = client.delete(
        "/delete/target",
        params={
            "upload_path": upload_path,
            "cleaned_path": cleaned_path
        }
    )

    # Validate response
    assert response.status_code == 200
    data = response.json()

    assert data["message"] == "File(s) deleted successfully"
    assert data["deleted_upload"] == upload_path
    assert data["deleted_cleaned"] == cleaned_path

    # Ensure files are deleted
    assert not os.path.exists(upload_path)
    assert not os.path.exists(cleaned_path)


def test_delete_files_nonexistent():
    # Paths that do not exist
    fake_upload = "/tmp/nonexistent_upload.csv"
    fake_cleaned = "/tmp/nonexistent_cleaned.csv"

    response = client.delete(
        "/delete/target",
        params={
            "upload_path": fake_upload,
            "cleaned_path": fake_cleaned
        }
    )

    # Should still return 200 because your endpoint ignores missing files
    assert response.status_code == 200
    data = response.json()

    assert data["message"] == "File(s) deleted successfully"
    assert data["deleted_upload"] == fake_upload
    assert data["deleted_cleaned"] == fake_cleaned
