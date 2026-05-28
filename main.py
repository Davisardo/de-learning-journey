# main.py — file utama yang menggunakan utils
from utils import validasi_nilai, hitung_total

transaksi = [15000, -5000, 25000, 0, 50000]

for nilai in transaksi:
    status = validasi_nilai(nilai)
    print(f"{nilai} - {status}")

total = hitung_total(transaksi)
print(f"\nTotal valid: {total}")