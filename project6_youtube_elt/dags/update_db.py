from airflow import DAG
import pendulum
from datetime import datetime, timedelta
from data_warehouse.data_warehouse import staging_table, core_table

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

with DAG(
    dag_id="update_db",
    default_args=default_args,
    description="This DAG processes the JSON file and inserts data into staging and core schemas",
    schedule="0 15 * * *",
    start_date=pendulum.datetime(2025, 1, 1, tz="Asia/Jakarta"),
    catchup=False,
) as dag:
    update_staging = staging_table()
    update_core = core_table()
    update_staging >> update_core