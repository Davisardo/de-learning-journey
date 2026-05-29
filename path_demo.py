import os
from pathlib import Path 

# Cek folder dan file
print(os.getcwd())                          # folder aktif sekarang
print(os.path.exists("data"))                # apakah folder data ada?
print(os.path.exists("data/transaksi.csv"))  # apakah file ada?

# List semua file di folder data
for file in os.listdir("data"):
    print(file)

# Buat folder baru kalau belum ada
os.makedirs("output", exist_ok=True)
print("Folder output siap")

# Pathlib — cara modern
path = Path("data/transaksi.csv")
print(path.name)        # nama file saja
print(path.stem)        # nama tanpa ekstensi
print(path.suffix)      # ekstensinya saja
print(path.parent)      # folder induknya
