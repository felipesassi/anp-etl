import pyspark.sql.types as T
import pyspark.sql.functions as F
from anp_etl.shared import get_spark_session


def select_cols_and_cast_types_to_ingestion(input_path: str, output_path: str) -> None:

    spark = get_spark_session()

    df = spark.read.option("sep", ";").option("header", "true").csv(input_path)

    df = df.withColumn("Data da Coleta", F.to_date("Data da Coleta", "dd/MM/yyyy"))
    df = df.withColumn("Valor de Compra", F.regexp_replace(F.col("Valor de Compra"), ",", "."))
    df = df.withColumn("Valor de Venda", F.regexp_replace(F.col("Valor de Venda"), ",", "."))

    col_types = {
        "Regiao - Sigla": T.StringType(),
        "Estado - Sigla": T.StringType(),
        "Municipio": T.StringType(),
        "Revenda": T.StringType(),
        "CNPJ da Revenda": T.StringType(),
        "Nome da Rua": T.StringType(),
        "Numero Rua": T.StringType(),
        "Complemento": T.StringType(),
        "Bairro": T.StringType(),
        "Cep": T.StringType(),
        "Bandeira": T.StringType(),
        "Produto": T.StringType(),
        "Unidade de Medida": T.StringType(),
        "Data da Coleta": T.DateType(),
        "Valor de Compra": T.DoubleType(),
        "Valor de Venda": T.DoubleType(),
    }

    for col in col_types:
        df = df.withColumn(col, F.col(col).cast(col_types[col]))

    df = df.withColumn("Year", F.year("Data da Coleta"))
    df = df.withColumn("Month", F.month("Data da Coleta"))

    (df.write.mode("overwrite").partitionBy("Year", "Month").format("parquet").save(output_path))
