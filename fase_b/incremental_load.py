import sqlite3
import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_max_user_id(conn, table_name):
    """Ambil user_id terbesar yang sudah ada di database"""
    try:
        result = pd.read_sql(
            f"SELECT MAX(user_id) as max_id FROM {table_name}", conn
        )
        return result["max_id"][0] or 0
    except:
        return 0

def incremental_load(filepath, db_path, table_name):
    conn = sqlite3.connect(db_path)
    
    # Cek data yang sudah ada
    max_id = get_max_user_id(conn, table_name)
    logging.info(f"User ID terakhir di database: {max_id}")
    
    # Baca data baru
    df_baru = pd.read_csv(filepath)
    
    # Filter hanya yang belum ada
    df_baru = df_baru[df_baru["user_id"] > max_id]
    logging.info(f"Data baru yang akan diload: {len(df_baru)} baris")
    
    if len(df_baru) > 0:
        df_baru.to_sql(table_name, conn, if_exists="append", index=False)
        logging.info("Incremental load selesai")
    else:
        logging.info("Tidak ada data baru")
    
    conn.close()

# Jalankan
incremental_load(
    "data/transaksi_baru.csv",
    "fase_b/pipeline.db",
    "transaksi"
)