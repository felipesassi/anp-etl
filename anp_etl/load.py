from anp_etl.shared import get_spark_session
from dotenv import load_dotenv
import os


load_dotenv()


def data_warehouse_path() -> str:

    return os.environ.get("DB_PATH", "localhost")


def load_anp_data_to_dw(input_path: str) -> None:

    spark = get_spark_session()

    df = spark.read.parquet(input_path)

    df = df.drop("Year", "Month")

    db_path = data_warehouse_path()

    (
        df.write.format("jdbc")
        .option("url", f"jdbc:postgresql://{db_path}:5432/postgres")
        .option("driver", "org.postgresql.Driver")
        .option("dbtable", os.environ.get("ANP_TABLE"))
        .mode("overwrite")
        .option("user", os.environ.get("DB_USER"))
        .option("password", os.environ.get("DB_PASSWORD"))
        .save()
    )


def load_gas_stations_data_to_dw(input_path: str) -> None:

    spark = get_spark_session()

    df = spark.read.parquet(input_path)

    db_path = data_warehouse_path()

    (
        df.write.format("jdbc")
        .option("url", f"jdbc:postgresql://{db_path}:5432/postgres")
        .option("driver", "org.postgresql.Driver")
        .option("dbtable", os.environ.get("GAS_STATIONS_TABLE"))
        .mode("overwrite")
        .option("user", os.environ.get("DB_USER"))
        .option("password", os.environ.get("DB_PASSWORD"))
        .save()
    )
