# Data Cleaner & Report Generator

A lightweight Python automation tool for cleaning messy CSV files, generating summary statistics, and exporting both a cleaned dataset and an HTML data report.

This project demonstrates practical data‑processing workflows commonly used in business analytics, operations, finance, and reporting automation.

---

## Features
- Load CSV datasets from a file path  
- Automatically handle missing values  
- Normalize and standardize column names  
- Remove duplicate records  
- Generate summary statistics  
- Export cleaned CSV files  
- Create a simple HTML analytics report  
- CLI‑based workflow (expandable to FastAPI)

---

## Tech Stack
- **Python 3**
- **pandas**
- **NumPy**
- **Jinja2** (optional, for HTML templating)
- **FastAPI** (optional API version)

---

## Project Structure
```bash
data-cleaner/
│
├── data/
│   ├── raw/
│   └── cleaned/
│
├── reports/
│   └── report.html
│
├── src/
│   ├── cleaner.py
│   ├── report_generator.py
│   └── main.py
│
├── requirements.txt
└── README.md
```
---

## Example Workflow

### Input CSV
Name,Age,Salary
John,29,50000
Sarah,,62000
Mike,35,

Code

### Automated Cleaning
- Fill missing numeric values  
- Normalize column names  
- Remove duplicates  
- Standardize formatting  

### Output — Cleaned CSV
name,age,salary
John,29,50000
Sarah,32,62000
Mike,35,56000

Code

### HTML Report Includes
- Dataset overview  
- Missing value analysis  
- Summary statistics  
- Column information  
- Basic visual insights  

---

## Installation

Clone the repository:
```bash
git clone https://github.com/azariah11dev/Data-Cleaner-Report-Generator.git
cd data-cleaner
Install dependencies:

bash
pip install -r requirements.txt
Usage
Run from CLI
bash
python src/main.py --input data/raw/sample.csv
Output Files
Cleaned CSV → data/cleaned/

HTML Report → reports/report.html

Example Summary Statistics
Rows Processed: 12,450

Columns: 18

Missing Values Fixed: 342

Duplicate Rows Removed: 27

Skills Demonstrated
Data cleaning with pandas

Automation scripting

File‑processing pipelines

Data validation

Report generation

Python project structuring

Business‑focused tooling

Potential Improvements
Drag‑and‑drop web interface

FastAPI upload endpoint

Interactive charts

Excel file support

AI‑generated data insights

Docker deployment

Why This Project Matters
Many businesses operate with inconsistent or incomplete spreadsheet data.
This tool automates repetitive cleanup tasks and produces easy‑to‑read reports, saving time for analysts and operations teams.

It reflects real‑world freelance work commonly requested on platforms like Upwork and Fiverr.

Author
Built by CodeArcade  
Open to freelance automation and data‑analytics projects.