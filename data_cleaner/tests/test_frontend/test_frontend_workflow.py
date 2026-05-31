import os
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "http://localhost:3000"


# ---------------------------------------------------------
# Test 1: Page Loads Correctly
# ---------------------------------------------------------
def test_page_loads(driver):
    driver.get(BASE_URL)
    assert "Document Cleaner" in driver.title


# ---------------------------------------------------------
# Test 2: Strategy Dropdown Contains Expected Values
# ---------------------------------------------------------
def test_strategy_dropdown(driver):
    driver.get(BASE_URL)

    dropdown = driver.find_element(By.ID, "strategy")
    options = [o.get_attribute("value") for o in dropdown.find_elements(By.TAG_NAME, "option")]

    expected = ["drop", "mean", "median", "mode", "constant", "ffill", "bfill"]
    assert options == expected


# ---------------------------------------------------------
# Test 3: Upload File Workflow
# ---------------------------------------------------------
def test_upload_file(driver, tmp_path):
    driver.get(BASE_URL)

    csv_path = tmp_path / "test.csv"
    csv_path.write_text("col1,col2\n1,a\n2,b\n")

    file_input = driver.find_element(By.ID, "fileInput")
    file_input.send_keys(str(csv_path))

    upload_btn = driver.find_element(By.ID, "upload-btn")
    upload_btn.click()

    # Wait until preview-container actually has content
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.ID, "preview-container"), "col1")
    )

    html = driver.find_element(By.ID, "preview-container").get_attribute("innerHTML")
    assert "col1" in html
    assert "col2" in html
    assert "1" in html


# ---------------------------------------------------------
# Test 4: Preview Is Generated
# ---------------------------------------------------------
def test_preview_generated(driver, tmp_path):
    driver.get(BASE_URL)

    csv_path = tmp_path / "preview.csv"
    csv_path.write_text("x,y\n10,20\n30,40\n")

    driver.find_element(By.ID, "fileInput").send_keys(str(csv_path))
    driver.find_element(By.ID, "upload-btn").click()

    # Wait until preview-container actually has content
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.ID, "preview-container"), "10")
    )

    html = driver.find_element(By.ID, "preview-container").get_attribute("innerHTML")
    assert "10" in html
    assert "20" in html


# ---------------------------------------------------------
# Test 5: Apply Cleaning Strategy
# ---------------------------------------------------------
def test_apply_cleaning(driver, tmp_path):
    driver.get(BASE_URL)

    csv_path = tmp_path / "clean.csv"
    csv_path.write_text("category,price\nA,10\n,20\nB,\n")

    driver.find_element(By.ID, "fileInput").send_keys(str(csv_path))
    driver.find_element(By.ID, "upload-btn").click()

    # Wait for upload + preview to complete before interacting
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.ID, "preview-container"), "category")
    )

    driver.find_element(By.ID, "strategy").send_keys("constant")
    driver.find_element(By.ID, "columns").send_keys("category")
    driver.find_element(By.ID, "fill-value").send_keys("Unknown")

    driver.find_element(By.ID, "apply-btn").click()

    # Wait until stats-container has the summary
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.ID, "stats-container"), "Cleaning Summary")
    )

    html = driver.find_element(By.ID, "stats-container").get_attribute("innerHTML")
    assert "Cleaning Summary" in html
    assert "Unknown" in html


# ---------------------------------------------------------
# Test 6: Download Button Exists and Is Clickable
# ---------------------------------------------------------
def test_download_button(driver):
    driver.get(BASE_URL)

    download_btn = driver.find_element(By.ID, "downloadBtn")
    assert download_btn.is_displayed()
    assert download_btn.is_enabled()

    download_btn.click()


# ---------------------------------------------------------
# Test 7: Delete Files Workflow
# ---------------------------------------------------------
def test_delete_files(driver, tmp_path):
    driver.get(BASE_URL)

    csv_path = tmp_path / "delete.csv"
    csv_path.write_text("a,b\n1,2\n")

    driver.find_element(By.ID, "fileInput").send_keys(str(csv_path))
    driver.find_element(By.ID, "upload-btn").click()

    # Wait for upload to finish before deleting
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.ID, "preview-container"), "a")
    )

    delete_btn = driver.find_element(By.ID, "deleteBtn")
    delete_btn.click()

    alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
    alert.accept()

    stats_html = driver.find_element(By.ID, "stats-container").get_attribute("innerHTML")
    assert stats_html.strip() == ""


# ---------------------------------------------------------
# Test 8: Constant Strategy Requires Value
# ---------------------------------------------------------
def test_constant_strategy_requires_value(driver, tmp_path):
    driver.get(BASE_URL)

    csv_path = tmp_path / "const.csv"
    csv_path.write_text("colA,colB\n1,2\n")

    driver.find_element(By.ID, "fileInput").send_keys(str(csv_path))
    driver.find_element(By.ID, "upload-btn").click()

    # Wait for upload to finish before interacting
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.ID, "preview-container"), "colA")
    )

    driver.find_element(By.ID, "strategy").send_keys("constant")
    driver.find_element(By.ID, "columns").send_keys("colA")
    # Leave fill-value EMPTY
    driver.find_element(By.ID, "apply-btn").click()

    alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
    text = alert.text.lower()
    alert.accept()

    assert "value" in text or "required" in text


# ---------------------------------------------------------
# Test 9: Invalid Column Handling
# ---------------------------------------------------------
def test_invalid_column(driver, tmp_path):
    driver.get(BASE_URL)

    csv_path = tmp_path / "invalid.csv"
    csv_path.write_text("colA,colB\n1,2\n3,4\n")

    driver.find_element(By.ID, "fileInput").send_keys(str(csv_path))
    driver.find_element(By.ID, "upload-btn").click()

    # Wait for upload to finish before interacting
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.ID, "preview-container"), "colA")
    )

    driver.find_element(By.ID, "strategy").send_keys("constant")
    driver.find_element(By.ID, "columns").send_keys("nonexistent_column")
    driver.find_element(By.ID, "fill-value").send_keys("X")

    driver.find_element(By.ID, "apply-btn").click()

    # Wait until stats-container has error content
    WebDriverWait(driver, 10).until(
        lambda d: d.find_element(By.ID, "stats-container").get_attribute("innerHTML").strip() != ""
    )

    stats_html = driver.find_element(By.ID, "stats-container").get_attribute("innerHTML").lower()
    assert "error" in stats_html or "invalid" in stats_html or "not found" in stats_html