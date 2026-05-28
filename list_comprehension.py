# Cara lama — for loop biasa
transaksi = [15000, -5000, 25000, -1000, 50000]

valid_lama = []
for nilai in transaksi:
    if nilai > 0:
        valid_lama.append(nilai)
print(valid_lama)

# Cara baru — list comprehension
valid_baru = [nilai for nilai in transaksi  if nilai > 0]
print(valid_baru)

nilai_abs = [abs(nilai) for nilai in transaksi]
print(nilai_abs)

kondisi = ["VALID" if nilai >= 0 else "INVALID" for nilai in transaksi]
print(kondisi)