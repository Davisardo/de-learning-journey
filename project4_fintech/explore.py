import pandas as pd

data = pd.read_csv("data/creditcard.csv")

print("=== CREDIT ===")
print(f"Shape: {data.shape}")  # jumlah baris & kolom
print(data.head(3))  # contoh isi data
print(data.dtypes)  # tipe data tiap kolom
print(data.isnull().sum().sum())  # total missing values
print(data["Class"].value_counts())  # jumlah normal vs fraud
print(data["Class"].value_counts(normalize=True) * 100)  # persentase normal vs fraud
