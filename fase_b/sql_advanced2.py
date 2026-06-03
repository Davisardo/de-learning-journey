import sqlite3
import pandas as pd

conn = sqlite3.connect("fase_b/toko_online.db")

# conn.executescript("""
#     DROP TABLE IF EXISTS pesanan;
#     DROP TABLE IF EXISTS produk;
#     DROP TABLE IF EXISTS pelanggan;

#     CREATE TABLE pelanggan (
#         pelanggan_id INTEGER PRIMARY KEY,
#         nama         TEXT,
#         kota         TEXT,
#         tier         TEXT,
#         tgl_daftar   TEXT
#     );

#     CREATE TABLE produk (
#         produk_id    INTEGER PRIMARY KEY,
#         nama_produk  TEXT,
#         kategori     TEXT,
#         harga        INTEGER,
#         stok         INTEGER
#     );

#     CREATE TABLE pesanan (
#         pesanan_id    INTEGER PRIMARY KEY,
#         pelanggan_id  INTEGER,
#         produk_id     INTEGER,
#         jumlah        INTEGER,
#         total_harga   INTEGER,
#         status        TEXT,
#         tgl_pesan     TEXT,
#         FOREIGN KEY (pelanggan_id) REFERENCES pelanggan(pelanggan_id),
#         FOREIGN KEY (produk_id)    REFERENCES produk(produk_id)
#     );

#     INSERT INTO pelanggan VALUES
#         (1,  'Rina',    'Surabaya', 'Gold',   '2024-01-10'),
#         (2,  'Fajar',   'Jakarta',  'Silver', '2024-02-15'),
#         (3,  'Dewi',    'Bandung',  'Gold',   '2024-01-20'),
#         (4,  'Hendra',  'Medan',    'Bronze', '2024-03-05'),
#         (5,  'Sari',    'Jakarta',  'Silver', '2024-02-28'),
#         (6,  'Arif',    'Surabaya', 'Bronze', '2024-04-01'),
#         (7,  'Putri',   'Yogya',    'Gold',   '2024-01-05'),
#         (8,  'Bagas',   'Bandung',  'Silver', '2024-03-18');

#     INSERT INTO produk VALUES
#         (1, 'Laptop Pro',    'Elektronik',   12000000, 10),
#         (2, 'Mouse Wireless','Elektronik',     250000, 50),
#         (3, 'Meja Belajar',  'Furnitur',      850000, 15),
#         (4, 'Kursi Ergonomis','Furnitur',    1500000, 8),
#         (5, 'Tas Ransel',    'Fashion',       350000, 30),
#         (6, 'Sepatu Lari',   'Fashion',       600000, 25),
#         (7, 'Buku Python',   'Buku',          120000, 100),
#         (8, 'Headphone',     'Elektronik',    800000, 20);

#     INSERT INTO pesanan VALUES
#         (1,  1, 1, 1, 12000000, 'Selesai',   '2026-01-03'),
#         (2,  1, 2, 2,   500000, 'Selesai',   '2026-01-05'),
#         (3,  2, 7, 3,   360000, 'Selesai',   '2026-01-03'),
#         (4,  3, 4, 1,  1500000, 'Selesai',   '2026-01-06'),
#         (5,  3, 1, 1, 12000000, 'Selesai',   '2026-01-08'),
#         (6,  4, 5, 2,   700000, 'Dikirim',   '2026-01-07'),
#         (7,  5, 8, 1,   800000, 'Selesai',   '2026-01-04'),
#         (8,  2, 1, 1, 12000000, 'Selesai',   '2026-01-09'),
#         (9,  6, 6, 1,   600000, 'Dikirim',   '2026-01-10'),
#         (10, 7, 3, 1,   850000, 'Selesai',   '2026-01-05'),
#         (11, 7, 4, 1,  1500000, 'Selesai',   '2026-01-06'),
#         (12, 8, 2, 3,   750000, 'Diproses',  '2026-01-11'),
#         (13, 1, 8, 1,   800000, 'Selesai',   '2026-01-12'),
#         (14, 5, 3, 1,   850000, 'Diproses',  '2026-01-11'),
#         (15, 3, 6, 2,  1200000, 'Dikirim',   '2026-01-13');
# """)

# conn.commit()
print("Database toko_online.db berhasil dibuat!")

df_check = pd.read_sql("SELECT COUNT(*) as total FROM pesanan", conn)
print(f"Total pesanan: {df_check['total'][0]} baris")
conn.close()

conn = sqlite3.connect("fase_b/toko_online.db")

# ── 1. JOIN 
print("=== JOIN: Detail Pesanan Lengkap ===")
df1 = pd.read_sql("""
    SELECT
        pe.pesanan_id,
        pl.nama AS nama_pelanggan,
        pl.kota,
        pr.nama_produk,
        pr.kategori,
        pe.jumlah,
        pe.total_harga,
        pe.status
    FROM pesanan pe
    JOIN pelanggan pl ON pe.pelanggan_id = pl.pelanggan_id
    JOIN produk pr ON pe.produk_id = pr.produk_id
    ORDER BY pe.pesanan_id
""",conn)
print(df1)

# ── 2. GROUP BY + HAVING ─────────────────────────────────────────
print("\n=== GROUP BY + HAVING: Pelanggan Belanja > 5 Juta ===")
df2 = pd.read_sql("""
        SELECT
            pl.nama,
            pl.tier,
            COUNT(pe.pesanan_id) AS jumlah_pesanan,
            SUM(pe.total_harga) AS total_belanja
        FROM pesanan pe
        JOIN pelanggan pl ON pe.pelanggan_id = pl.pelanggan_id
        GROUP BY pl.nama, pl.tier
        HAVING total_belanja > 5000000
        ORDER BY total_belanja DESC    
""", conn)
print(df2)

# ── 3. WINDOW FUNCTIONS ──────────────────────────────────────────
print("\n=== WINDOW FUNCTIONS: Peringkat & Total Per Pelanggan ===")
df3 = pd.read_sql("""
    SELECT
        pl.nama,
        pr.nama_produk,
        pe.total_harga,
        SUM (pe.total_harga) OVER (PARTITION BY pl.pelanggan_id)
            AS total_belanja_pelanggan,
        RANK() OVER (ORDER BY pe.total_harga DESC)
            AS peringkat_transaksi
    FROM pesanan pe
    JOIN pelanggan pl ON pe.pelanggan_id = pl.pelanggan_id
    JOIN produk pr ON pe.produk_id = pr.produk_id
""",conn)
print(df3)

# ── 4. CTE ───────────────────────────────────────────────────────
print("\n=== CTE: Ringkasan Belanja Per Kota ===")
df4 = pd.read_sql("""
    WITH ringkasan AS(
        SELECT
            pl.kota,
            COUNT(pe.pesanan_id) AS jumlah_pesanan,
            SUM(pe.total_harga) AS total_omzet,
            AVG(pe.total_harga) AS rata_nilai_pesanan
        FROM pesanan pe
        JOIN pelanggan pl ON pe.pelanggan_id = pl.pelanggan_id
        GROUP BY pl.kota
    )
    SELECT
        kota,
        jumlah_pesanan,
        total_omzet,
        ROUND(rata_nilai_pesanan) AS rata_nilai_pesanan
    FROM ringkasan
    ORDER BY total_omzet DESC
""",conn)
print(df4)