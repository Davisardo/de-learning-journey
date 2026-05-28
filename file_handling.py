# # Baca file CSV secara manual
# file = open("data/transaksi.csv", "r")
# isi = file.read()
# file.close()

# print(isi)

# Cara yang lebih baik - with statement
# with open("data/transaksi.csv", "r") as file:
#     isi = file.read()

# print(isi)

# with open("data/transaksi.csv", "r") as file:
#     for baris in file:
#         print(baris)

with open("data/transaksi.csv", "r") as file:
    #Skip baris pertama (header)
    header = file.readline()

    for baris in file:
        kolom =  baris.strip().split(",")
        user_id = kolom[0]
        nama = kolom[1]
        nilai = int(kolom[2])

        if nilai > 0:
            print(f"{nama} - VALID: {nilai}")
        elif nilai == 0:
            print(f"{nama} - PERLU DICEK")
        else:
            print(f"{nama} - INVALID: {nilai}")



