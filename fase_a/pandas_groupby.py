import pandas as pd

# Baca hasil merge yang sudah kita buat
df = pd.read_csv("output/hasil_merge.csv")
print(df)
print("---")

# GroupBy — total transaksi per kategori
hasil = df.groupby("kategori")["nilai_transaksi"].sum()
print(hasil)
print("---")

# GroupBy dengan multiple agregasi
hasil2 = df.groupby("kategori")["nilai_transaksi"].agg(["sum", "mean", "count"])
print(hasil2)

# GroupBy dengan multiple agregasi
hasil3 = df.groupby("nama")["nilai_transaksi"].agg(["sum", "mean", "count"])
print(hasil3)
