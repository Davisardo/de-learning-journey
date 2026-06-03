from datetime import datetime

# Simulasi XCom — tanpa Airflow
# Di Airflow nyata, ini ditangani otomatis oleh framework


def extract(**context):
    """Extract data dan push ke XCom"""
    data = [15000, -5000, 25000, 0, 50000]

    # Di Airflow: context['ti'].xcom_push(key='raw_data', value=data)
    print(f"Extract selesai - {len(data)} baris")
    return data  # return value otomatis jadi XCom


def transform(**context):
    """Ambil data dari XCom dan transform"""
    # Di Airflow: data = context['ti'].xcom_pull(task_ids='extract')
    data = context.get("raw_data", [])

    hasil = [x for x in data if x > 0]
    print(f"Transform selesai - {len(hasil)} baris valid")
    return hasil


def load(**context):
    """Ambil hasil transform dan load"""
    data = context.get("valid_data", [])
    print(f"Load selesai - {len(data)} baris diload")


# Simulasi pipeline dengan XCom
print("=== Simulasi XCom Pipeline ===")
raw_data = extract()
valid_data = transform(raw_data=raw_data)
load(valid_data=valid_data)
