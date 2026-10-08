# Banking Data Engineering Pipeline

An end-to-end banking data engineering pipeline built using **Apache Airflow, Docker, Snowflake, and dbt**.

The project follows the **Medallion Architecture** to ingest raw banking transaction data, transform it into a dimensional model, and generate business-ready analytics and KPIs.

---

## 1. Project Overview

This project demonstrates a complete data engineering workflow:

```text
CSV Dataset
     |
     v
Apache Airflow
     |
     v
Snowflake Stage
     |
     v
Bronze Layer
     |
     v
dbt Staging
     |
     v
Silver Layer
     |
     v
Gold Layer
     |
     v
Business KPIs