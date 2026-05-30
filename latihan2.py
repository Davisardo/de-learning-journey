def cek_status(nilai):
    if nilai > 0:
        return "VALID"
    elif nilai == 0:
        return "PERLU DICEK"
    else:
        return "INVALID"

print(cek_status(15000))
print(cek_status(-3000))
print(cek_status(0))


with open("data/transaksi.csv","r") as file:
    skip = file.readline()
    for baris in file:
        kolom = baris.strip().split(",")
        nama = kolom[1]
        nilai = int(kolom[2])
        print(f"nama: {nama}|nilai: {nilai}")



