# Modern Data Stack — Overview

stack = {
    "ingestion": {
        "tools": ["Fivetran", "Airbyte", "custom Python script"],
        "fungsi": "Ambil data dari berbagai sumber ke data lake/warehouse",
        "yang_kita_pakai": "Custom Python script (ETL pipeline kita)"
    },
    "storage": {
        "tools": ["BigQuery", "Snowflake", "Redshift", "S3"],
        "fungsi": "Simpan data mentah dan hasil transformasi",
        "yang_kita_pakai": "SQLite (simulasi lokal)"
    },
    "transformation": {
        "tools": ["dbt", "Spark"],
        "fungsi": "Transform data di dalam warehouse",
        "yang_kita_pakai": "dbt (sudah buat model)"
    },
    "orchestration": {
        "tools": ["Airflow", "Prefect", "Dagster"],
        "fungsi": "Schedule dan monitor pipeline",
        "yang_kita_pakai": "Airflow (sudah buat DAG konsep)"
    },
    "visualization": {
        "tools": ["Looker Studio", "Metabase", "Superset", "Tableau"],
        "fungsi": "Dashboard dan reporting",
        "yang_kita_pakai": "Belum — akan di Fase D"
    }
}

for layer, detail in stack.items():
    print(f"\n{'='*40}")
    print(f"Layer: {layer.upper()}")
    print(f"Tools: {', '.join(detail['tools'])}")
    print(f"Fungsi: {detail['fungsi']}")
    print(f"Kita pakai: {detail['yang_kita_pakai']}")