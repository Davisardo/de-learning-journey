nama_kolom = "user_id"
jumlah_transaksi = 1500
nilai_trasanksi = 99500.50
data_valid = True

print(type(nama_kolom))
print(type(jumlah_transaksi))
print(type(nilai_trasanksi))
print(type(data_valid))

harga_dari_csv = "99500"
diskon_dari_csv = "0.1"
jumlah_dari_csv = "5"

harga = int(harga_dari_csv)
jumlah = int(jumlah_dari_csv)
diskon = float(diskon_dari_csv)

total = harga * jumlah
print(total)

harga_setelah_diskon = harga - (harga * diskon)
print(harga_setelah_diskon)

print(int("0.1"))
