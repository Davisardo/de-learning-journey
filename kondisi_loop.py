# Simulasi data transaksi dari pipeline
transaksi = [15000, -5000, 25000, 0, 50000, -1000]

for nilai in transaksi:
    if nilai > 0:
        print(f"{nilai} - VALID")
    elif nilai == 0:
        print(f"{nilai} - PERLU DICEK")
    else:
        print(f"{nilai} - INVALID")

total = 0
for nilai in transaksi:
    if nilai > 0:
        total = total + nilai

print(f"Total transaksi valid: {total}")
