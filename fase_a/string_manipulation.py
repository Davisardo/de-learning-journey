# Simulasi data kotor dari pipeline
nama = "  john doe  "
email = "john.doe@gmail.com"
tanggal = "2024-01-15"
harga = "Rp 99.500"

# 1. Hapus spasi di depan dan belakang
nama_bersih = nama.strip()
print(nama_bersih)

# 2. Ubah jadi huruf kapital semua
nama_upper = nama_bersih.upper()
print(nama_upper)

# 3. Ambil username dari email (sebelum @)
username = email.split("@")[0]
print(username)

# 4. Pisah tanggal
bagian_tanggal = tanggal.split("-")
print(bagian_tanggal)

# 5. Hapus karakter tidak perlu
harga_bersih = harga.replace("Rp ", "").replace(".", "")
print(harga_bersih)

tahun = tanggal.split("-")[0]
print(tahun)

take_gmail = email.split("@")[1].split(".")[0]
print(take_gmail)
