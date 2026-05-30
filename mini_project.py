import pandas as pd
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
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

ringkasan = df.groupby("status")["nilai_transaksi"].agg(["sum","mean","count"])

ringkasan.to_csv("output/laporan_ringkasan.csv", index=True)

logging.info("Pipeline selesai - laporan tersimpan di output/laporan_ringkasan.csv")