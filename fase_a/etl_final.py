import sqlite3
import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

df = pd.read_csv("data/transaksi.csv")


def cek_status(nilai):
    if nilai > 0:
        return "VALID"
    elif nilai == 0:
        return "PERLU DICEK"
    else:
        return "INVALID"


df["status"] = df["nilai_transaksi"].apply(cek_status)

try:
    conn = sqlite3.connect("data/etl_final.db")
    logging.info("Koneksi berhasil")
    df.to_sql("transaksi", conn, if_exists="replace", index=False)
    logging.info(f"Data diload: {len(df)} baris")
    df_verify = pd.read_sql("SELECT * FROM transaksi", conn)
    print(df_verify)
    conn.close()
    logging.info("Selesai")
except Exception as e:
    logging.error(f"Pipeline gagal: {e}")
