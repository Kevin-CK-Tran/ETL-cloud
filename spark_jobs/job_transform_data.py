from pyspark.sql import SparkSession
import argparse
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def transform_data (spark, input_path, output_path):
    logger.info(f'Reading raw data from {input_path}')
    df = spark.read.option('header', True).csv(input_path)
    
    logger.info('Initial schema:')
    df.printSchema()
    
    logger.info('Preview of raw data:')
    df.show(5)
    
    # Combine all csv files to 1 single file
    logger.info(f'Combine files and write to {output_path}')
    df.coalesce(1).write.mode('overwrite').option('header', True).csv(output_path)
    
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