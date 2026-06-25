import pandas as pd
import logging
from google.cloud import bigquery
from transform import (
    load_data,
    create_fact_shipments,
    create_dim_carrier,
    create_dim_route,
)

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# CONNECT - buat client sekali di luar fungsi
PROJECT_ID = "amplified-ward-416314"
DATASET = "routewise_logistics"
client = bigquery.Client(project=PROJECT_ID)


def load_to_bigquery(df, table_name, write_mode="WRITE_TRUNCATE"):
    # STEP 1 - DEFINE TARGET
    table_id = f"{PROJECT_ID}.{DATASET}.{table_name}"

    # STEP 2 - SET JOB CONFIG
    job = client.load_table_from_dataframe(
        df,
        table_id,
        job_config=bigquery.LoadJobConfig(write_disposition=write_mode),
    )

    # STEP 3 - LOAD
    job.result()
    logger.info(
        f" [LOADED] {table_name}: {len(df):,} baris berhasil di-load (mode: {write_mode})"
    )

    # STEP 4 - VERIFY & LOGGING
    table = client.get_table(table_id)
    logger.info(f"[LOADED] {table_name}: {len(df):,} baris dikirim")
    logger.info(f"[VERIFY] {table_name}: {table.num_rows:,} baris di Bigquery")


if __name__ == "__main__":
    # PREPARE DATA
    df = load_data()
    fact_shipments = create_fact_shipments(df)
    dim_carrier = create_dim_carrier(df)
    dim_route = create_dim_route(df)

    load_to_bigquery(fact_shipments, "fact_shipments")
    load_to_bigquery(dim_carrier, "dim_carrier")
    load_to_bigquery(dim_route, "dim_route")
