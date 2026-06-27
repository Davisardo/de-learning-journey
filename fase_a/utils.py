# utils.py — kumpulan function reusable

def validasi_nilai(nilai):
    if nilai > 0:
        return "VALID"
    elif nilai == 0:
        return "PERLU DICEK"
    else:
        return "INVALID"

def hitung_total(list_nilai):
    return sum([n for n in list_nilai if n > 0])