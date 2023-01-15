from pyspark.sql import SparkSession


def get_spark_session() -> SparkSession:

    spark = (
        SparkSession.builder.master("local[*]")
        .appName("ANP-Pipeline")
        .config("spark.jars", "./jars/postgresql-42.5.1.jar")
        .config("spark.sql.sources.partitionOverwriteMode", "dynamic")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("ERROR")

    return spark


spark = get_spark_session()
