from datetime import datetime, timedelta

# Simulasi struktur DAG Airflow
# (tanpa install Airflow dulu)

dag_config = {
    "dag_id": "etl_transaksi_harian",
    "schedule": "0 6 * * *",  # setiap hari jam 6 pagi
    "start_date": datetime(2026, 1, 1),
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}

# Task-task dalam pipeline
tasks = [
    {"task_id": "extract_data", "operator": "PythonOperator", "fungsi": "extract()"},
    {
        "task_id": "transform_data",
        "operator": "PythonOperator",
        "fungsi": "transform()",
    },
    {"task_id": "load_data", "operator": "PythonOperator", "fungsi": "load()"},
]

# Urutan eksekusi
print(f"DAG: {dag_config['dag_id']}")
print(f"Jadwal: {dag_config['schedule']}")
print(f"Retry: {dag_config['retries']}x dengan jeda {dag_config['retry_delay']}")
print("\nUrutan task:")
for i, task in enumerate(tasks):
    if i < len(tasks) - 1:
        print(f"  {task['task_id']} >> {tasks[i + 1]['task_id']}")
