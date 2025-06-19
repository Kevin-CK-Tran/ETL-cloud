import os
import yaml
import subprocess

# Setup logger
from utils.logger import get_logger
logger = get_logger(__name__)

# Load configuration from YAML file
def load_config(config_path='configs/config.yaml'):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)
    
def run_spark_job(config):
    spark_config = config['spark']
    input_path = spark_config['input_path']
    output_path = spark_config['output_path']
    
    os.makedirs(output_path, exist_ok=True)
    
    # Define the Spark submit command
    spark_job_path = 'spark_jobs/job_transform_data.py'
    
    command = [
        'spark-submit', spark_job_path,
        '--input', input_path,
        '--output', output_path
    ]
    
    logger.info(f'Running Spark job with command: {" ".join(command)}')
    
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        logger.info(f'Spark job completed successfully:\n{result.stdout}')
        
    except subprocess.CalledProcessError as e:
        logger.error(f'Spark job failed:\n{e.stderr}')
        raise
    
# This is the function that Airflow DAG will call
def transform_with_spark():
    config = load_config()
    run_spark_job(config)

# Optional for standalone manual testing    
if __name__ = "__main__":
    transform_with_spark()