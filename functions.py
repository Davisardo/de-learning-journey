# # Tanpa function — kode berulang
transaksi_januari = [15000, -5000, 25000]
transaksi_februari = [30000, -2000, 10000]
transaksi_maret = [45000, -1500, 47000]
# # Validasi januari
# for nilai in transaksi_januari:
#     if nilai >0:
#         print(f"{nilai} - VALID")
#     else:
#         print(f"{nilai} - INVALID")

# # Validasi februari - kode yang sama diulang lagi
# for nilai in transaksi_februari:
#     if nilai >0:
#         print(f"{nilai} - VALID")
#     else:
#         print(f"{nilai} - INVALID")

# Dengan function - tulis sekali, pakai berkali kali
# def validasi_transaksi(list_transaksi):
#     for nilai in list_transaksi:
#         if nilai > 0:
#           print(f"{nilai} - VALID")
#         else:
#             print(f"{nilai} - INVALID")

# # Panggil function untuk setiap bulan
# validasi_transaksi(transaksi_januari)
# validasi_transaksi(transaksi_februari)
# validasi_transaksi(transaksi_maret)

def hitung_total_valid(list_transaksi):
    total = 0
    for nilai in list_transaksi:
        if nilai > 0:
            total = total + nilai
    return total

# Panggil dan simpan hasilnya
total_januari = hitung_total_valid(transaksi_januari)
total_februari = hitung_total_valid(transaksi_februari)
gabungan = total_januari + total_februari

print(f"Total valid Januari: {total_januari}")
print(f"Total valid Februari: {total_februari}")
print(f"Total valid Gabungan: {gabungan}")