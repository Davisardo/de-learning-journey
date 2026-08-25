from airflow import DAG
import pendulum
from datetime import datetime, timedelta
from api.video_stats import get_playlist_id, get_video_id, extract_video_data, save_to_json


default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

with DAG(
    dag_id="generate_json",
    default_args=default_args,
    description="This DAG is to generate a JSON file with raw data",
    schedule="0 14 * * *",
    start_date=pendulum.datetime(2025, 1, 1, tz="Asia/Jakarta"),
    catchup=False,
) as dag:
    playlist_id_task = get_playlist_id()
    video_id_task = get_video_id(playlist_id_task)
    extracted_data_task = extract_video_data(video_id_task)
    save_json_task = save_to_json(extracted_data_task)




