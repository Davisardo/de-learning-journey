import pandas as pd

# Baca dua dataset
df_transaksi = pd.read_csv("data/transaksi.csv")
df_kategori = pd.read_csv("data/kategori.csv")

print(df_transaksi)
print("---")
print(df_kategori)

df_merge = pd.merge(df_transaksi, df_kategori, on="user_id", how="left")
print(df_merge)

# Isi NaN dengan nilai default
df_merge["kategori"] = df_merge["kategori"].fillna("Unknown")
print(df_merge)

# Export hasil ke CSV
df_merge.to_csv("output/hasil_merge.csv", index=False)
print("Exported ke output/hasil_merge.csv")
