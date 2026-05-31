import os
import time
import socket
import subprocess
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import shutil


# ---------------------------------------------------------
# Helper: Wait for a port to open
# ---------------------------------------------------------
def wait_for_port(host, port, timeout=15):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except OSError:
            time.sleep(0.3)
    raise RuntimeError(f"Server {host}:{port} did not start in time")


# ---------------------------------------------------------
# Fixture: Start FastAPI Backend
# ---------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def start_backend():
    # Absolute path to project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    # Backend directory
    backend_dir = os.path.join(project_root, "src", "backend")
    backend_app = "app:app"

    process = subprocess.Popen(
        ["uvicorn", backend_app, "--host", "127.0.0.1", "--port", "8000"],
        cwd=backend_dir
    )

    wait_for_port("127.0.0.1", 8000)
    yield
    process.terminate()


# ---------------------------------------------------------
# Fixture: Start Express Frontend
# ---------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def start_frontend():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    process = subprocess.Popen(
        ["node", "server.js"],
        cwd=project_root
    )

    wait_for_port("127.0.0.1", 3000)
    yield
    process.terminate()


# ---------------------------------------------------------
# Fixture: Selenium WebDriver
# ---------------------------------------------------------
@pytest.fixture(scope="session")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()


@pytest.fixture(scope="session", autouse=True)
def cleanup_backend_files():
    yield  # wait until ALL tests finish

    # Paths where backend stores files
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    backend_dir = os.path.join(project_root, "src", "backend")

    upload_dir = os.path.join(backend_dir, "models", "upload_csv")
    cleaned_dir = os.path.join(backend_dir, "models", "save_csv")

    # Remove folders if they exist
    for folder in [upload_dir, cleaned_dir]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
