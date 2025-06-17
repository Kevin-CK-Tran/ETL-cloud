# ETL Pipeline: S3 → Spark → Snowflake

This project implements a cloud-based ETL pipeline that extracts data from AWS S3, transforms it using Apache Spark, and loads the results into Snowflake. The pipeline is orchestrated using Apache Airflow and can run in a Dockerized environment.

---

## 🗂️ Project Structure

etl_pipeline_first_cloud/
├── dags/
│   └── etl_pipeline_dag.py           # Airflow DAG for orchestrating the ETL
│
├── configs/
│   └── config.yaml                   # Configuration for S3, Spark, Snowflake
│
├── data/
│   ├── raw/                          # Local backup of raw data from S3 (optional)
│   └── processed/                    # Local backup of processed data (optional)
│
├── scripts/
│   ├── extract/
│   │   └── s3_extractor.py           # Logic to download data from S3
│   │
│   ├── transform/
│   │   └── spark_transformer.py      # Spark jobs to clean/transform data
│   │
│   └── load/
│       └── snowflake_loader.py       # Logic to load data into Snowflake
│
├── spark_jobs/
│   └── job_transform_data.py         # Main PySpark script called by spark_transformer
│
├── utils/
│   ├── logger.py                     # Custom logging utility
│   └── snowflake_connector.py        # Reusable connection logic for Snowflake
│
├── requirements.txt                  # Python dependencies
├── Dockerfile                        # Docker setup (if containerized)
├── docker-compose.yaml               # Airflow + Spark environment orchestration
└── README.md                         # Project documentation


---

## ⚙️ Features

- **Extract** data from AWS S3
- **Transform** using Apache Spark (PySpark)
- **Load** into Snowflake data warehouse
- **Schedule** and orchestrate jobs with Apache Airflow
- **Dockerized** setup for local development/testing

---

## 🧪 Technologies Used

- **Python 3.9+**
- **Apache Spark**
- **Snowflake**
- **Apache Airflow**
- **Docker + Docker Compose**
- **AWS S3**
- **PyYAML** for config parsing

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Docker & Docker Compose
- AWS credentials configured
- Snowflake account with credentials

### Installation

```bash
# Clone the repo
git clone https://github.com/your-username/etl_pipeline_first_cloud.git
cd etl_pipeline_first_cloud

# Create a virtual environment (optional)
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt


# Docker Setup

# Build and start the services
docker-compose up --build

Airflow will be accessible at: http://localhost:8080
Default credentials: airflow / airflow


# Configuration
Edit configs/config.yaml with your S3 bucket, Snowflake account, and other settings.

s3:
  bucket_name: your-bucket
  file_key: path/to/data.csv

spark:
  app_name: etl_spark_job

snowflake:
  user: YOUR_USER
  password: YOUR_PASSWORD
  account: YOUR_ACCOUNT
  warehouse: YOUR_WAREHOUSE
  database: YOUR_DB
  schema: YOUR_SCHEMA
  table: YOUR_TABLE


📅 Airflow DAG
The DAG is defined in dags/etl_pipeline_dag.py. It performs:

1- Extract from S3

2- Transform using Spark

3- Load to Snowflake


📂 Local Data Backups (Optional)

Raw S3 data: data/raw/

Processed output: data/processed/


🛠️ Development
Use logger.py for consistent logging

Use snowflake_connector.py for reusing connection logic


🧪 Testing
pytest


🧾 License
This project is licensed under the MIT License.


📧 Contact
For questions or support, reach out at [your-email@example.com]


