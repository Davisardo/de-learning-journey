# import sqlite3
# import pandas as pd
# import logging

# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )

# # Buat koneksi ke database SQLite
# conn = sqlite3.connect("data/pipeline.db")
# logging.info("Koneksi ke database berhasil")

# # Buat tabel transaksi
# conn.execute("""
#         CREATE TABLE IF NOT EXISTS transaksi (
#             user_id INTEGER,
#             nama TEXT,
#             nilai_transaksi INTEGER,
#             status TEXT
#         )
# """)

# logging.info("Tabel transaksi siap")

# # Tutup koneksi
# conn.close()
# logging.info("Koneksi ditutup")


import sqlite3
import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

conn = sqlite3.connect("data/pipeline.db")
logging.info("Koneksi ke databse berhasil")

conn.execute("""
    CREATE TABLE IF NOT EXISTS transaksi (
        user_id INTEGER,
        nama TEXT,
        nilai_transaksi INTEGER,
        status TEXT
    )
""")

# Baca CSV dan masukkan ke database
df = pd.read_csv("data/transaksi.csv")


def cek_status(nilai):
    if nilai > 0:
        return "VALID"
    elif nilai == 0:
        return "PERLU DICEK"
    else:
        return "INVALID"


df["status"] = df["nilai_transaksi"].apply(cek_status)

# Load ke database
df.to_sql("transaksi", conn, if_exists="replace", index=False)
logging.info(f"Data berhasil diload: {len(df)} baris")

# Baca kembali dari database untuk verifikasi
df_verify = pd.read_sql("SELECT * FROM transaksi", conn)
print(df_verify)

conn.close()
logging.info("Koneksi ditutup")
