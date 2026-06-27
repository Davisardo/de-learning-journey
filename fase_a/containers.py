# LIST — data transaksi harian
transaksi = [15000, 25000, 15000, 50000, 25000]
print(transaksi)
print(len(transaksi))

# TUPLE — konfigurasi koneksi database (tidak boleh diubah)
db_config = ("localhost", 5432, "mydb")
print(db_config)

# DICTIONARY — satu record data user
user = {
    "user_id": 101,
    "nama": "Davis",
    "kota": "Surabaya"
}
print(user["nama"])

# SET — hapus duplikat dari transaksi
transaksi_unik = set(transaksi)
print(transaksi_unik)

transaksi.append(75000)
print(transaksi)

user["email"] = "davis@gmail.com"
print(user) 