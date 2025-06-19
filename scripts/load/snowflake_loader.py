import os
import logging
from glob import glob

from utils.snowflake_connector import get_snowflake_connection, load_config  # ✅ Imported from connector

# Setup logger
from utils.logger import get_logger
logger = get_logger(__name__)

# Load CSV files into Snowflake
def load_csv_to_snowflake(config):
    sf_config = config['snowflake']
    processed_path = config['spark']['output_path']
    table_name = sf_config['table']

    # Get all CSV files in processed folder
    csv_files = glob(os.path.join(processed_path, '*.csv'))
    if not csv_files:
        logger.info(f'No csv files found in {processed_path}')
        return

    conn = get_snowflake_connection(config)  # ✅ Reuse connector logic
    cursor = conn.cursor()

    try:
        logger.info("Creating a temporary stage...")
        cursor.execute("CREATE OR REPLACE TEMPORARY STAGE temp_football_stage")

        for file_path in csv_files:
            file_name = os.path.basename(file_path)

            logger.info(f"Uploading {file_name} to Snowflake stage...")
            put_cmd = f'PUT file://{file_path} @temp_football_stage OVERRIDE = TRUE'
            cursor.execute(put_cmd)

            logger.info(f"Copying {file_name} from stage to table {table_name}...")
            copy_cmd = f"""
                COPY INTO {table_name}
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
    config = load_config()  # ✅ Reuse loader from connector
    load_csv_to_snowflake(config)

# Optional manual test
if __name__ == '__main__':
    load_to_snowflake()