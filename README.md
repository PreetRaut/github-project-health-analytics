# GitHub Analytics with dbt

An analytics engineering project that transforms GitHub repository data into business-ready insights using dbt, DuckDB, and GitHub APIs.

## Project Overview

This project demonstrates modern analytics engineering practices by:

- Extracting repository data from GitHub APIs
- Storing raw data in DuckDB
- Transforming data using dbt
- Creating clean analytics models
- Generating documentation and lineage graphs
- Producing insights about repository activity and contributors

The goal is to simulate a real-world analytics engineering workflow similar to those used by data teams at technology companies.

---

## Tech Stack

- Python
- DuckDB
- dbt Core
- dbt-duckdb
- GitHub REST API
- SQL
- Git

---

## Project Structure

```text
github-analytics-dbt/
│
├── data/
│   └── raw/
│
├── dbt_project/
│   ├── models/
│   │   ├── staging/
│   │   ├── marts/
│   │   └── schema.yml
│   │
│   ├── analyses/
│   ├── tests/
│   └── dbt_project.yml
│
├── ingest_github.py
├── requirements.txt
├── README.md
└── github_analytics.duckdb
```

---

## Data Source

This project uses the GitHub REST API.

Example repository:

```text
microsoft/playwright
```

Data collected:

- Repository metadata
- Stars
- Forks
- Open issues
- Pull requests
- Contributors
- Repository activity

---

## Analytics Questions Answered

### Repository Performance

- Which repositories have the most stars?
- Which repositories are growing fastest?
- What is the star-to-fork ratio?

### Contributor Insights

- Top contributors by commits
- Most active repositories
- Contribution distribution

### Development Activity

- Open vs closed pull requests
- Issue activity
- Repository engagement metrics

---

## Setup Instructions

### Clone Repository

```bash
git clone https://github.com/yourusername/github-analytics-dbt.git
cd github-analytics-dbt
```

### Create Virtual Environment

Mac/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Load Data

Run:

```bash
python ingest_github.py
```

This will:

1. Call GitHub APIs
2. Retrieve repository information
3. Store raw data in DuckDB

---

## Run dbt Models

Navigate to dbt project:

```bash
cd dbt_project
```

Run transformations:

```bash
dbt run
```

Run tests:

```bash
dbt test
```

Generate documentation:

```bash
dbt docs generate
```

Launch docs site:

```bash
dbt docs serve
```

---

## Example Models

### Staging Layer

- stg_repositories
- stg_contributors

Purpose:
- Rename columns
- Standardize formats
- Clean raw API data

### Mart Layer

- repository_summary
- contributor_summary

Purpose:
- Business-friendly reporting tables
- Aggregated metrics
- KPI calculations

---

## Example Metrics

| Metric | Description |
|----------|-------------|
| Total Stars | Repository popularity |
| Total Forks | Repository adoption |
| Open Issues | Development workload |
| Contributors | Community engagement |
| Stars per Contributor | Efficiency metric |

---

## Data Quality Tests

Implemented using dbt:

- Not Null Tests
- Unique Tests
- Accepted Values Tests
- Relationship Tests

Example:

```yaml
tests:
  - unique
  - not_null
```

---

## Skills Demonstrated

### Analytics Engineering

- Data Modeling
- SQL Transformations
- ETL Pipelines
- Data Quality Testing
- Documentation

### Data Engineering

- API Integration
- Python Automation
- DuckDB
- Data Storage

### Business Intelligence

- KPI Development
- Reporting Models
- Data Storytelling

---

## Future Improvements

- GitHub Actions CI/CD
- Incremental Models
- dbt Snapshots
- Multiple Repository Support
- Power BI Dashboard
- Streamlit Analytics Dashboard

---

