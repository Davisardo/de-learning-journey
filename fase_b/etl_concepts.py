import sqlite3
import pandas as pd
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def extract(filepath):
    """Baca data dari CSV"""
    logging.info(f"Extracting data dari {filepath}")
    df = pd.read_csv(filepath)
    logging.info(f"Extracted {len(df)} baris")
    return df


def transform(df):
    """Transform data"""
    logging.info("Transforming data")
    df["status"] = df["nilai_transaksi"].apply(
        lambda x: "VALID" if x > 0 else ("PERLU DICEK" if x == 0 else "INVALID")
    )
    df["processed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return df


def load(df, db_path, table_name):
    """Load data ke database"""
    try:
        conn = sqlite3.connect(db_path)
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        logging.info(f"Loaded {len(df)} baris ke tabel {table_name}")
        conn.close()
    except Exception as e:
        logging.error(f"Load gagal: {e}")
        raise


def run_pipeline():
    logging.info("Pipeline dimulai")
    df = extract("data/transaksi.csv")
    df = transform(df)
    load(df, "fase_b/pipeline.db", "transaksi")
    logging.info("Pipeline selesai")


run_pipeline()
