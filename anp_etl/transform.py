import pyspark.sql.types as T
import pyspark.sql.functions as F
from pyspark.sql.window import Window 
from anp_etl.shared import get_spark_session


def create_lag_price_and_lag_date_table(input_path, output_path):

    spark = get_spark_session()

    df = spark.read.parquet(input_path)

    w = Window().partitionBy("CNPJ da Revenda", "Produto").orderBy("Data da Coleta")

    df = df.withColumn("Valor de Venda Anterior", F.lag("Valor de Venda").over(w))
    df = df.withColumn("Data da Coleta Anterior", F.lag("Data da Coleta").over(w))

    df = df.withColumn("Dias entre Coletas", F.datediff(F.col("Data da Coleta"), F.col("Data da Coleta Anterior")))

    df = df.withColumn("Year", F.year("Data da Coleta"))
    df = df.withColumn("Month", F.month("Data da Coleta"))

    (df
        .write
        .mode("overwrite")
        .partitionBy("Year", "Month")
        .format("parquet")
        .save(output_path)
    )


def create_gas_stations_table(input_path, output_path):

    spark = get_spark_session()

    df = spark.read.parquet(input_path)

    w = Window().partitionBy("CNPJ da Revenda").orderBy(F.col("Data da Coleta").desc())

    df = df.withColumn("row_number", F.row_number().over(w))

    df = df.filter(F.col("row_number") == 1)

    cols_to_use = [
        "Regiao - Sigla",
        "Estado - Sigla",
        "Municipio",
        "Revenda",
        "CNPJ da Revenda",
        "Nome da Rua",
        "Numero Rua",
        "Complemento",
        "Bairro",
        "Cep",
        "Bandeira",
    ]

    df = df.select(*cols_to_use)

    (df
        .write
        .mode("overwrite")
        .format("parquet")
        .save(output_path)
    )

