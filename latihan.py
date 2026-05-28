total_valid = 0
total_invalid = 0
total_perlu_dicek = 0

with open("data/transaksi.csv", "r") as transaksi:
    header = transaksi.readline()

    for baris in transaksi:
        kolom = baris.strip().split(",")
        nama = kolom[1]
        nilai = int(kolom[2])
        if nilai > 0:
            total_valid = total_valid + nilai
        elif nilai == 0:
            total_perlu_dicek = total_perlu_dicek + nilai
        else:
            total_invalid = total_invalid + nilai

with open("ringkasan.txt", "w") as hasil:
    hasil.write(f"Total transaksi valid: {total_valid}\n")
    hasil.write(f"Total transaksi invalid: {total_invalid}\n")
    hasil.write(f"Total transaksi perlu dicek: {total_perlu_dicek}\n")
    
