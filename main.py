from loguru import logger
from anp_etl.download import get_tables_to_download, download_raw_data
from anp_etl.extract import select_cols_and_cast_types_to_ingestion
from anp_etl.transform import create_lag_price_and_lag_date_table, create_gas_stations_table
from anp_etl.load import load_anp_data_to_dw, load_gas_stations_data_to_dw
from anp_etl.shared import get_spark_session
from anp_etl.validation import configure_great_expectations, get_batch_request, run_great_expectations_checkpoint
from dotenv import load_dotenv
import os


load_dotenv()

   
def main():

    logger.info("Get tables to download")
    
    tables = get_tables_to_download()

    logger.info(f"Found {tables.shape[0]} to download from ANP data portal")

    [run_data_pipeline(tables, i) for i in range(tables.shape[0])]


def run_data_pipeline(tables, i):

    logger.info("Download and save ANP data")

    path = download_raw_data(tables, i)

    logger.info(f"Path - {path} found to download data")

    validate_and_process_raw_data(path)


def validate_and_process_raw_data(path):

    spark = get_spark_session()

    df = spark.read.option("header", True).option("sep", ";").csv(path)


    logger.info("Configuring great expectations context/suite")

    context = configure_great_expectations()

    batch_request = get_batch_request(df, path.split("/")[-1].split(".")[0])


    logger.info("Run great expectations checkpoint in raw data")

    run_great_expectations_checkpoint(context, batch_request)


    logger.info("Process raw data from bronze layer to silver layer")

    select_cols_and_cast_types_to_ingestion(path, f"{os.environ.get('SILVER_PATH')}/anp_raw")



    logger.info("Process ingested data to gold layer to create table with lags")

    create_lag_price_and_lag_date_table("data/silver/anp_raw", f"{os.environ.get('GOLD_PATH')}/anp")



    logger.info("Process ingested data to gold layer to create gas station table")

    create_gas_stations_table("data/silver/anp_raw", f"{os.environ.get('GOLD_PATH')}/gas_stations")


    logger.info("Saving ANP data to data warehouse")

    load_anp_data_to_dw(f"{os.environ.get('GOLD_PATH')}/anp")


    logger.info("Saving gas stations data to data warehouse")

    load_gas_stations_data_to_dw(f"{os.environ.get('GOLD_PATH')}/gas_stations")