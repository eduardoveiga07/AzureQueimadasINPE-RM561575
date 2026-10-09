from pyspark.sql.types import (
    StructType, StructField, StringType, DoubleType, TimestampType, LongType
)

# Caminho direto do Unity Catalog Volume — sem parametro, sem dbfs:
VOLUME_PATH = "/Volumes/inpe/bronze/arquivo"

schema = StructType([
    StructField("id", StringType()),
    StructField("lat", DoubleType()),
    StructField("lon", DoubleType()),
    StructField("data_hora_gmt", TimestampType()),
    StructField("satelite", StringType()),
    StructField("municipio", StringType()),
    StructField("estado", StringType()),
    StructField("pais", StringType()),
    StructField("municipio_id", LongType()),
    StructField("estado_id", LongType()),
    StructField("pais_id", LongType()),
    StructField("numero_dias_sem_chuva", LongType()),
    StructField("precipitacao", DoubleType()),
    StructField("risco_fogo", DoubleType()),
    StructField("bioma", StringType()),
    StructField("frp", DoubleType()),
])

df_bronze = (
    spark.read
    .option("header", True)
    .option("encoding", "UTF-8")
    .schema(schema)
    .csv(VOLUME_PATH)
)

display(df_bronze)
df_bronze.printSchema()

df_bronze.write.format("delta").mode("overwrite") \
    .saveAsTable("inpe.bronze.focos_raw")
