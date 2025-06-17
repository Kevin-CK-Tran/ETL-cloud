from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from scripts.extract.s3_extractor import extract_from_s3
from scripts.transform.spark_transformer import transform_with_spark
from scripts.load.snowflake_loader import load_to_snowflake

default_args = {
    'owner': 'airflow',
    'depend_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2025,1,1)
}

with DAG(
    dag_id = 'S3_to_Snowflake',
    default_args = default_args,
    schedule_interval = '@daily',
    catchup = False,
    description = 'ETL pipeline from S3 to Snowflake via Spark'
) as dag:
    
    extract_task = PythonOperator(
        task_id = 'extract_from_s3',
        python_callable = extract_from_s3
    )
    
    transform_task = PythonOperator(
        task_id = 'transform_with_spark',
        python_callable = transform_with_spark
    )
    
    load_task = PythonOperator(
        task_id = 'load_to_snowflake',
        python_callable = load_to_snowflake
    )
    
    extract_task >> transform_task >> load_task