import pandas as pd 

# Baca CSV — satu baris, bukan 5 baris seperti sebelumnya
df = pd.read_csv("data/transaksi.csv")

# Lihat isinya
print(df)
print("---")

# Info dasar
print(df.shape)         # berapa baris dan kolom
print(df.columns)       # nama kolom
print(df.dtypes)         # tipe data setiap kolom

# Filtering — ambil hanya transaksi valid
df_valid = df[df["nilai_transaksi"] > 0]
print(df_valid)
print("---")

# Sorting — urutkan dari terbesar
df_sorted = df.sort_values("nilai_transaksi", ascending=False)
print(df_sorted)
print("---")

# Agregasi — hitung total dan rata-rata
print(f"Total valid: {df_valid['nilai_transaksi'].sum()}")
print(f"Rata-rata: {df['nilai_transaksi'].mean()}")

def cek_status(nilai):
    if nilai > 0:
        return "VALID"
    elif nilai == 0:
        return "PERLU DICEK"
    else:
        return "INVALID"

df["status"] = df["nilai_transaksi"].apply(cek_status)
print(df)

pd.set_option("display.max_columns", None)
print(df)