import os 
import boto3
import yaml
import logging
from botocore.exceptions import BotoCoreError, ClientError

# Setup logger
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(_name_)

# Load configuration from YAML file
def load_config(config_path='configs/config.yaml'):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)
    
# Core logic: download files from S3
def download_files_from_s3(config):
    s3_config = config['s3']
    bucket = s3_config['bucket']
    prefix = s3_config['prefix']
    download_path = s3_config['download_path']
    
    os.makedirs(download_path, exist_ok=True)
    s3 = boto3.client('s3') # Create a connection with AWS calling to S3 service 
    
    try:
        response = s3.list_objects_v2(Bucket = bucket, Prefix = prefix)
        
        if 'Contents' not in response:
            logger.info("No files exist in bucket KevinTran")
            return
        
            # It will return like this:
            # {
            # "Contents": [
            # {"Key": "raw-data/score1.csv", "Size": 123},
            # {"Key": "raw-data/score2.csv", "Size": 456}
            # ],
            # ...
            # }    
            
        for obj in response['Contents']:
            key = obj['Key'] 
            filename = os.path.basename(key) # From "raw-data/score1.csv" will return only "score1.csv" as the filename 
            if not filename: # If filename is empty, meaning from "raw-data/" -> no file inside this folder raw-data -> meaning it's just a folder 
                continue # For that case, skip the folder name 
            
            # Now download to the pre-defined download folder in config.yaml: /opt/airflow/data/raw/ -> folder inside the container
            download_folder_container = os.path.join(download_path, filename) # -> /opt/airflow/data/raw/score1.csv
            logger.info(f'Downloading {key} to {download_folder_container}')
            
            # Execute the download to container folder
            s3.download_file(bucket, key, download_folder_container)
            
        logger.info("All files downloaded successfully")
        
    except (BotoCoreError, ClientError) as e:
        logger.error(f"Failed to download files from S3: {error}")
        raise
            
# Last function - This is the function that Airflow DAG will call
def extract_from_s3():
    config = load_config()
    download_files_from_s3(config)
    
# Optional for standalone manual testing - Directly execute this file
if __name__ == "__main__":
    extract_from_s3()