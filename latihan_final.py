import sqlite3
import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

df = pd.read_csv("data/penjualan.csv")

df["total_harga"] = df["jumlah"] * df["harga_satuan"]


def cek_status(jumlah):
    if jumlah > 0:
        return "TERJUAL"
    elif jumlah == 0:
        return "KOSONG"
    else:
        return "ERROR DATA"


df["status"] = df["jumlah"].apply(cek_status)

ringkasan = df.groupby("kategori")["total_harga"].agg(["sum", "mean", "count"])

try:
    conn = sqlite3.connect("data/penjualan.db")
    logging.info("Koneksi berhasil")
    df.to_sql("penjualan", conn, if_exists="replace", index=False)
    logging.info(f"Data diload: {len(df)} baris")
    df_verify = pd.read_sql("SELECT * FROM penjualan", conn)
    print(df_verify)
    conn.close()
    logging.info("Selesai")
except Exception as e:
    logging.error(f"Pipeline gagal: {e}")

ringkasan.to_csv("output/ringkasan_penjualan.csv", index=True)
