from google.cloud import bigquery
import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


PROJECT_ID = "amplified-ward-416314"
DATASET_ID = "de_learning"


client = bigquery.Client(project=PROJECT_ID)
logging.info("Koneksi ke BigQuery berhasil")

# Buat tabel transaksi di BiqQuery
table_id = f"{PROJECT_ID}.{DATASET_ID}.transaksi"

schema = [
    bigquery.SchemaField("user_id", "INTEGER"),
    bigquery.SchemaField("nama", "STRING"),
    bigquery.SchemaField("nilai_transaksi", "INTEGER"),
    bigquery.SchemaField("status", "STRING"),
]

table = bigquery.Table(table_id, schema=schema)

try:
    table = client.create_table(table)
    logging.info(f"Tabel {table_id} berhasil dibuat")
except Exception as e:
    logging.info(f"Tabel sudah ada: {e}")

# Load data dari CSV ke BigQuery

df = pd.read_csv("data/transaksi.csv")
df["status"] = df["nilai_transaksi"].apply(
    lambda x: "VALID" if x > 0 else ("PERLU DICEK" if x == 0 else "INVALID")
)

job = client.load_table_from_dataframe(df, table_id)
job.result()
logging.info(f"Data berhasil diload ke BigQuery: {len(df)} baris")


# Query dari BigQuery
query = f"""
    SELECT status, COUNT(*) as jumlah, SUM(nilai_transaksi) as total
    FROM `{table_id}`
    GROUP BY status
    ORDER BY total DESC
"""

df_result = client.query(query).to_dataframe()
print(df_result)
logging.info("Query selesai")
