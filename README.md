# Data Cleaner & Report Generator API

A FastAPI-powered backend service that automates spreadsheet cleaning, validation, and export workflows.

Designed for analysts, operations teams, finance professionals, and businesses that regularly work with CSV or Excel data.

---

## Overview

The API provides a simple workflow:

1. Upload a dataset
2. Clean and standardize the data
3. Preview results
4. Download the cleaned file

The service is designed to eliminate repetitive spreadsheet cleanup tasks and improve data quality before reporting or analytics.

---

## Features

- CSV and Excel file support
- Missing value handling
- Duplicate removal
- Column normalization
- Data preview endpoints
- Cleaned file export
- RESTful API architecture
- FastAPI validation and error handling

---

## Base URL

```http
http://localhost:8000
```

---

## Health Check

### Request

```http
GET /health
```

### Response

```json
{
  "status": "healthy"
}
```

---

# API Workflow

---

## 1. Upload Dataset

Upload a CSV or Excel file for processing.

### Request

```http
POST /cleaner/upload
```

### Example Response

```json
{
  "message": "File uploaded successfully",
  "file_name": "sales_data.csv"
}
```

---

## 2. Clean Dataset

Run automated cleaning operations on the uploaded file.

### Request

```http
POST /cleaner/clean
```

### Cleaning Operations

- Handle missing values
- Remove duplicates
- Normalize column names
- Standardize formatting

### Example Response

```json
{
  "message": "Cleaning completed",
  "rows_processed": 12450,
  "duplicates_removed": 27,
  "missing_values_fixed": 342,
  "output_file": "cleaned_sales_data.csv"
}
```

---

## 3. Preview Cleaned Data

Preview processed records without downloading the full file.

### Request

```http
GET /live-update/preview?file_name=cleaned_sales_data.csv
```

### Example Response

```json
{
  "columns": [
    "customer_name",
    "order_date",
    "revenue"
  ],
  "preview": [
    {
      "customer_name": "John Smith",
      "order_date": "2025-01-01",
      "revenue": 100.00
    }
  ]
}
```

---

## 4. Download Cleaned Dataset

Download the cleaned output file.

### Request

```http
GET /live-update/download?file_path=cleaned_sales_data.csv
```

### Response

Returns the processed CSV file.

---

## 5. Delete Dataset

Remove uploaded files from storage.

### Request

```http
DELETE /delete/target
```

### Example Response

```json
{
  "message": "File deleted successfully"
}
```

---

# Root Endpoint

### Request

```http
GET /
```

### Response

Returns API metadata and available routes.

```json
{
  "message": "Welcome to Quant Calc!",
  "description": "Backend server for Quant Calc."
}
```

---

# Example Use Cases

This API can be used for:

- Business data cleanup
- Financial reporting pipelines
- CRM export standardization
- Power BI preprocessing
- Excel workflow automation
- Data quality validation
- Internal reporting systems

---

# Technology Stack

## Backend

- FastAPI
- Pydantic v2
- Python 3.13

## Data Processing

- pandas
- NumPy

## File Handling

- pathlib
- python-multipart

## Testing

- pytest
- pytest-anyio
- httpx

---

# Local Development

Install dependencies:

```bash
uv sync
```

Start the server:

```bash
uvicorn app.main:app --reload
```

Open API documentation:

```text
http://localhost:8000/docs
```

ReDoc documentation:

```text
http://localhost:8000/redoc
```

---

# Business Value

Organizations frequently spend hours manually cleaning spreadsheet exports before they can be used for reporting, dashboards, or analytics.

This API automates that process by providing a repeatable, scalable data-cleaning workflow that reduces manual effort and improves data consistency.

---

# Author

**CodeArcade**

Python Automation • Data Engineering • Backend Development

Available for freelance projects involving:

- Data cleaning
- API development
- Business automation
- Reporting pipelines
- Analytics tooling