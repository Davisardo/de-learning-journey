from google.cloud import bigquery
import pandas as pd
import logging
from transform import (
    load_data,
    create_dim_orders,
    create_fact_payments,
    create_dim_customers,
    create_dim_products,
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

PROJECT_ID = "amplified-ward-416314"
DATASET_ID = "de_learning"
client = bigquery.Client(project=PROJECT_ID)


def load_to_bigquery(df, table_name):
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"
    job = client.load_table_from_dataframe(
        df, table_id,
        job_config=bigquery.LoadJobConfig(
            write_disposition="WRITE_TRUNCATE"  # timpa tabel setiap run
        )
    )
    job.result()
    logging.info(f"Loaded {len(df)} baris ke {table_id}")


if __name__ == "__main__":
    logging.info("Load ke BigQuery dimulai")

    orders, payments, customers, products = load_data()  # baca 4 CSV mentah

    # ubah jadi fact & dimension table
    dim_orders = create_dim_orders(orders)
    fact_payments = create_fact_payments(payments)
    dim_customers = create_dim_customers(customers)
    dim_product = create_dim_products(products)

    load_to_bigquery(dim_orders, "dim_orders")
    load_to_bigquery(fact_payments, "fact_payments")
    load_to_bigquery(dim_customers, "dim_customers")
    load_to_bigquery(dim_product, "dim_products")

    logging.info("Selesai")