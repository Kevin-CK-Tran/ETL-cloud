from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import argparse

# Setup logging
from utils.logger import get_logger
logger = get_logger(__name__)

column_mapping = {
    "ID": "ID",
    "Club": "CLUB",
    "Nationality": "NATIONALITY",
    "Matches played": "MATCHES_PLAYED",
    "Won": "WON",
    "Drawn": "DRAWN",
    "Lost": "LOST",
    "Possesion (%)": "POSSESSION",
    "Passing accuracy (%)": "PASSING_ACCURACY"
}

def transform_data (spark, input_path, output_path):
    logger.info(f'Reading raw data from {input_path}')
    df = spark.read.option('header', True).csv(input_path)
    
    logger.info('Initial schema:')
    df.printSchema()
    
    logger.info('Preview of raw data:')
    df.show(5)
    
    #Map the columns:
    mapped_df = df.select([col(old).alias(new) for old, new in column_mapping.item()])
    
    logger.info('Transformed Data Preview:')
    mapped_df.show(5)
    
    # Combine all csv files to 1 single file
    logger.info(f'Combine files and write to {output_path}')
    mapped_df.coalesce(1).write.mode('overwrite').option('header', True).csv(output_path)
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help='Input path to raw CSV files')
    parser.add_argument('--output', required=True, help='Output path for cleaned CSV files')
    args = parser.parse_args()

    logger.info('Starting Spark transformation job...')
    spark = SparkSession.builder.appName('ETL Spark job to Snowflake').getOrCreate()
    
    transform_data(spark, args.input, args.output)
    
    spark.stop()
    logger.info('Spark job completed.')
    
if __name__ == "__main__":
    main()