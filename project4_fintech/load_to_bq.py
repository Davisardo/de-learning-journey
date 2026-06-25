from google.cloud import bigquery
import pandas as pd
import logging
from transform import (
    build_dim_time,
    build_dim_amount,
    build_dim_fraud,
    build_dim_features,
    build_fact_transaction,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

PROJECT_ID = "amplified-ward-416314"
DATASET_ID = "fintrack_fraud"
client = bigquery.Client(project=PROJECT_ID)


def load_full(df, table_name):
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"
    job = client.load_table_from_dataframe(
        df,
        table_id,
        job_config=bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE"),
    )
    job.result()
    logging.info(f"Loaded {len(df)} baris ke {table_id} (WRITE_TRUNCATE)")


def get_last_id(table_name):
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"
    query = f"SELECT MAX(transaction_id) as max_id FROM `{table_id}`"
    try:
        result = client.query(query).result()
        row = list(result)[0]
        last_id = row.max_id
        if last_id is None:
            return -1
        return last_id
    except Exception as e:
        logging.info(f"Tabel belum ada atau kosong: {e}")
        return -1


def load_incremental(df, table_name):
    logging.info(f"Memulai proses incremental load untuk tabel: {table_name}")
    last_id = get_last_id(table_name)
    logging.info(f"ID terakhir yang ada di BigQuery ({table_name}): {last_id}")

    new_data = df[df["transaction_id"] > last_id]

    if not new_data.empty:
        table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"
        job = client.load_table_from_dataframe(
            new_data,
            table_id,
            job_config=bigquery.LoadJobConfig(write_disposition="WRITE_APPEND"),
        )
        job.result()
        logging.info(f"Sukses! {len(new_data)} baris baru ditambahkan ke {table_id}.")
    else:
        logging.info("Tidak ada data baru. BigQuery sudah up-to-date.")


if __name__ == "__main__":
    logging.info("Pipeline load ke BigQuery dimulai")

    data = pd.read_csv("data/credit/creditcard.csv")
    data = data.drop_duplicates()

    data, dim_time = build_dim_time(data)
    data, dim_amount = build_dim_amount(data)
    data, dim_fraud = build_dim_fraud(data)
    data, dim_features = build_dim_features(data)
    data, fact_transaction = build_fact_transaction(data)

    # Dim tables: full load, boleh ditimpa
    load_full(dim_time, "dim_time")
    load_full(dim_amount, "dim_amount")
    load_full(dim_fraud, "dim_fraud")
    load_full(dim_features, "dim_features")

    # Fact table: incremental load
    load_incremental(fact_transaction, "fact_transactions")

    logging.info("Pipeline selesai")
