import sqlite3
import pandas as pd

# Buat database dengan data yang lebih kaya
conn = sqlite3.connect("fase_b/sql_practice.db")

# Buat tabel dan isi data
# conn.executescript("""
#     DROP TABLE IF EXISTS transaksi;
#     DROP TABLE IF EXISTS users;
    
#     CREATE TABLE users (
#         user_id INTEGER,
#         nama TEXT,
#         kota TEXT,
#         kategori TEXT
#     );
    
#     CREATE TABLE transaksi (
#         trx_id INTEGER,
#         user_id INTEGER,
#         produk TEXT,
#         nilai INTEGER,
#         tanggal TEXT
#     );
    
#     INSERT INTO users VALUES 
#         (1, 'Davis', 'Surabaya', 'Premium'),
#         (2, 'Andi', 'Jakarta', 'Regular'),
#         (3, 'Budi', 'Surabaya', 'Premium'),
#         (4, 'Citra', 'Bandung', 'Regular'),
#         (5, 'Deni', 'Jakarta', 'Premium');
    
#     INSERT INTO transaksi VALUES
#         (1, 1, 'Laptop', 8000000, '2026-01-01'),
#         (2, 1, 'Mouse', 150000, '2026-01-02'),
#         (3, 2, 'Keyboard', 300000, '2026-01-01'),
#         (4, 3, 'Monitor', 2500000, '2026-01-03'),
#         (5, 3, 'Laptop', 8000000, '2026-01-04'),
#         (6, 4, 'Mouse', 150000, '2026-01-02'),
#         (7, 5, 'Monitor', 2500000, '2026-01-03'),
#         (8, 2, 'Laptop', 8000000, '2026-01-05');
# """)

# conn.commit()
print("Database siap")
conn.close()

conn = sqlite3.connect("fase_b/sql_practice.db")

# 1. JOIN — gabungkan users dan transaksi
print ("=== JOIN ===")
df = pd.read_sql("""
    SELECT
        t.trx_id,          
        u.nama,
        u.kota,
        t.produk,
        t.nilai
    FROM transaksi t
    JOIN users u ON t.user_id = u.user_id                 
""",conn)
print(df)

# 2. GROUP BY dan HAVING
print("=== GROUP BY dan HAVING ===")
df2 = pd.read_sql("""
        SELECT
            u.nama,
            COUNT(t.trx_id) as jumlah_transaksi,
            SUM(t.nilai) as total_nilai
    FROM transaksi t
    JOIN users u ON t.user_id = u.user_id
    GROUP BY u.nama
    HAVING total_nilai > 1000000
    ORDER BY total_nilai DESC
""", conn)
print(df2)

# 3. Window Functions
print("=== WINDOW FUNCTIONS ===")
df3 = pd.read_sql("""
        SELECT
            u.nama,
            t.produk,
            t.nilai,
            SUM(t.nilai) OVER (PARTITION BY u.nama) as total_per_user,
            RANK() OVER (ORDER BY t.nilai DESC) as rangking
        FROM transaksi t
        JOIN users u ON t.user_id = u.user_id
""", conn)
print(df3)