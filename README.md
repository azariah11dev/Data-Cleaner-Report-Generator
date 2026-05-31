# Data Cleaner & Report Generator

A full-stack data processing application that automates spreadsheet cleaning, validation, and export workflows.

Built for analysts, operations teams, finance professionals, and businesses that regularly work with CSV or Excel data.

The application combines a FastAPI backend, a lightweight frontend interface, automated testing, and data-processing pipelines to eliminate repetitive spreadsheet cleanup tasks.

---

## 🎥 Demo Video

Watch the full project walkthrough here:

**YouTube Demo:**  
[Insert YouTube Link Here](https://youtube.com/)

---

# Project Overview

Messy spreadsheets create unnecessary work before data can be used for reporting, dashboards, analytics, or decision-making.

This application provides a streamlined workflow:

1. Upload a CSV or Excel file
2. Preview the original dataset
3. Apply cleaning operations
4. Preview the cleaned dataset
5. Download the processed file
6. Remove files when finished

The goal is to automate repetitive data-cleaning tasks and improve data quality before analysis.

---

# Features

## Data Processing

- CSV file support
- Excel file support (.xlsx, .xls)
- Missing value handling
- Duplicate record removal
- Column normalization
- Data validation
- Export cleaned datasets

## Cleaning Strategies

Supported missing-value strategies:

- Drop Rows
- Mean
- Median
- Mode
- Constant Value
- Forward Fill
- Backward Fill

Users can apply cleaning operations globally or target specific columns.

---

## API Features

- File upload endpoint
- Dataset preview endpoint
- Automated cleaning endpoint
- File download endpoint
- File deletion endpoint
- Health monitoring endpoint
- Interactive Swagger documentation

---

## Frontend Features

- File upload interface
- Original dataset preview
- Cleaning strategy selection
- Custom column targeting
- Cleaned dataset preview
- Download functionality
- File management controls

---

# Example Workflow

## Input Dataset

| Name | Age | Salary |
|--------|--------|--------|
| John | 29 | 50000 |
| Sarah | NULL | 62000 |
| Mike | 35 | NULL |

---

## Cleaning Operations

- Handle missing values
- Remove duplicates
- Standardize formatting
- Normalize column names

---

## Output Dataset

| name | age | salary |
|--------|--------|--------|
| John | 29 | 50000 |
| Sarah | 32 | 62000 |
| Mike | 35 | 56000 |

---

# API Endpoints

## Upload Dataset

```http
POST /cleaner/upload
```

Uploads a CSV or Excel file for processing.

---

## Clean Dataset

```http
POST /cleaner/clean
```

Runs automated cleaning operations against the uploaded dataset.

---

## Preview Dataset

```http
GET /live-update/preview?file_name=<filename>
```

Returns a preview of the selected dataset.

---

## Download Dataset

```http
GET /live-update/download?file_path=<file_path>
```

Downloads the cleaned file.

---

## Delete Files

```http
DELETE /delete/target
```

Removes uploaded and processed files from storage.

---

## Health Check

```http
GET /health
```

Returns service health status.

---

# Technology Stack

## Backend

- Python 3.13
- FastAPI
- Pydantic v2
- pandas
- NumPy

## Frontend

- Express.js
- Vanilla JavaScript
- HTML5
- CSS3

## File Handling

- pathlib
- python-multipart

## Testing

- pytest
- pytest-anyio
- httpx
- Selenium

---

# Testing

The project includes automated backend and frontend testing.

### Test Coverage

- API endpoint testing
- File upload workflows
- Data cleaning operations
- Error handling
- Dataset preview functionality
- File download functionality
- Frontend user workflows
- End-to-end Selenium testing

### Run All Tests

```bash
uv run pytest
```

### Run Backend Tests

```bash
uv run pytest tests/test_backend
```

### Run Frontend Tests

```bash
uv run pytest tests/test_frontend
```

---

# Installation

Clone the repository:

```bash
git clone https://github.com/azariah11dev/Data-Cleaner-Report-Generator.git
cd Data-Cleaner-Report-Generator
```

Install dependencies:

```bash
uv sync
```

---

# Running the Application

The project includes a PowerShell launcher that starts both the backend and frontend automatically.

From the project root:
```bash
cd data_cleaner
```
then:
```bash
.\runApp.ps1
```

The launcher will:

- Start FastAPI (Port 8000)
- Start Express.js (Port 3000)
- Open the application in your browser
- Keep both services running until terminated

To stop the application:

```powershell
CTRL + C
```

---

# Development

## Backend

Start FastAPI manually:
navigate to:
```bash
 cd data_cleaner/src/backend
 ```
then
```bash
uv run main.py
```

Swagger Documentation:

```text
http://localhost:8000/docs
```

ReDoc Documentation:

```text
http://localhost:8000/redoc
```

---

## Frontend

Start Express manually:
navigate to:
```bash
cd data_cleaner
```
then:
```bash
node server.js
```

---

# Example Use Cases

This application can be used for:

- Business data cleanup
- Financial reporting workflows
- CRM export standardization
- Power BI preprocessing
- Excel automation
- Data quality validation
- Internal analytics pipelines
- Operations reporting

---

# Business Value

Organizations frequently spend hours manually cleaning spreadsheet exports before they can be used for dashboards, reporting, or analysis.

This application automates that process by providing a repeatable and scalable workflow that:

- Improves data quality
- Reduces manual effort
- Standardizes datasets
- Accelerates reporting workflows
- Increases operational efficiency

---

# Author

## CodeArcade

Python Automation • Data Engineering • Backend Development

Available for freelance projects involving:

- Data cleaning
- API development
- Business automation
- Reporting pipelines
- Analytics tooling

GitHub:
https://github.com/azariah11dev