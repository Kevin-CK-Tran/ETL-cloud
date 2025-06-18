import os
import yaml
import logging
import snowflake.connector
from glob import glob

# Setup logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load configuration from YAML
def load_config(config_path='configs/config.yaml'):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)
    
# Establish connection to Snowflake
def get_snowflake_connection(config):
    sf_config = config['snowflake']
    return snowflake.connector.connect(
        user = sf_config['user'],
        password = sf_config['password'],
        account = sf_config['account'],
        warehouse = sf_config['warehouse'],
        database = sf_config['database'],
        schema = sf_config['schema'],
        role = sf_config['role']
    )
    
# Load CSV files into Snowflake
def load_csv_to_snowflake(config):
    sf_config = config['snowflake']
    processed_path = config['spark']['output_path']
    table = sf_config['table']
    
    # Get all CSV files in processed folder
    csv_files = glob(os.path.join(processed_path, '*.csv'))
    if not csv_files:
        logger.info(f'No csv files found in {processed_path}')
        return
    
    conn = get_snowflake_connection(config)
    cursor = conn.cursor()
    
    try:
        # Create a temporary stage (if not exists)
        logger.info("Creating a temporary stage...")
        cursor.execute("CREATE OR REPLACE TEMPORARY STAGE temp_football_stage")
        
        # Upload and load each CSV
        for file_path in csv_files:
            file_name = os.path.basename(file_path)
            
            logger.info(f"Uploading {file_name} to Snowflake stage...")
            put_cmd = f'PUT file://{file_path} @temp_football_stage OVERRIDE = TRUE'
            cursor.execute(put_cmd)
            
            logger.info(f"Copying {file_name} from stage to table {table_name}...")
            copy_cmd = f"""
                COPY INTO {table}
                FROM @temp_football_stage/{file_name}
                FILE_FORMAT = (TYPE = CSV FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1)
                ON_ERROR = 'CONTINUE'
            """
            cursor.execute(copy_cmd)
            
        logger.info("All files loaded into Snowflake successfully.")
        
    except Exception as e:
        logger.error(f"Error loading data to Snowflake: {e}")
        raise
    
    finally:
        cursor.close()
        conn.close()
        
# Main callable for Airflow
def load_to_snowflake():
    config = load_config()
    load_csv_to_snowflake(config)

# Optional manual test
if __name__ == '__main__':
    load_to_snowflake()