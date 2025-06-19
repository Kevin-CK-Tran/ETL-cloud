import yaml
import snowflake.connector

# Setup logger
from utils.logger import get_logger
logger = get_logger(__name__)

def load_config(config_path='configs/config.yaml'):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def get_snowflake_connection(config=None):
    """
    Establish and return a Snowflake connection using configuration.
    If config not provided, load from default config.yaml.
    """
    if config is None:
        config = load_config()

    sf_config = config['snowflake']

    try:
        conn = snowflake.connector.connect(
            user=sf_config['user'],
            password=sf_config['password'],
            account=sf_config['account'],
            warehouse=sf_config['warehouse'],
            database=sf_config['database'],
            schema=sf_config['schema'],
            role=sf_config['role']
        )
        logger.info("Successfully connected to Snowflake")
        return conn

    except Exception as e:
        logger.error(f"Failed to connect to Snowflake: {e}")
        raise

# Optional test block
if __name__ == '__main__':
    config = load_config()
    conn = get_snowflake_connection(config)
    print("Connection successful!" if conn else "Connection failed.")
    conn.close()
