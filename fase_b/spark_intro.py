from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, sum, count, avg
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Buat SparkSession — ini entry point ke Spark
spark = SparkSession.builder \
    .appName("DE Learning Pipeline") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")
logging.info("SparkSession berhasil dibuat")

# Baca CSV dengan Spark
df = spark.read.csv("data/transaksi.csv", header=True, inferSchema=True)
logging.info(f"Data dibaca: {df.count()} baris")

# Tampilkan schema
df.printSchema()

# Tampilkan data
df.show()


# Transform dengan Spark — mirip Pandas tapi distributed
from pyspark.sql.functions import when, col

df_transform = df.withColumn(
    "status",
    when(col("nilai_transaksi") > 0, "VALID")
    .when(col("nilai_transaksi") == 0, "PERLU DICEK")
    .otherwise("INVALID")
)

df_transform.show()

# Agregasi
df_transform.groupBy("status").agg(
    {"nilai_transaksi": "sum"}
).show()

spark.stop()
