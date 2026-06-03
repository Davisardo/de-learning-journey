import sqlite3
import pandas as pd

conn = sqlite3.connect("fase_b/warehouse.db")

# Buat Star Schema
conn.executescript("""
    DROP TABLE IF EXISTS dim_customer;
    DROP TABLE IF EXISTS dim_produk;
    DROP TABLE IF EXISTS fact_transaksi;

    -- Dimension Table: Customer
    CREATE TABLE dim_customer (
        customer_id INTEGER PRIMARY KEY,
        nama TEXT,
        kota TEXT,
        kategori TEXT
    );
    
    -- Dimension Table: Produk
    CREATE TABLE dim_produk (
        produk_id INTEGER PRIMARY KEY,
        nama_produk TEXT,
        kategori_produk TEXT,
        harga_satuan INTEGER
    );

    -- Fact Table: Transaksi
    CREATE TABLE fact_transaksi (
        trx_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        produk_id INTEGER,
        jumlah INTEGER,
        total_nilai INTEGER,
        tanggal TEXT,
        FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
        FOREIGN KEY (produk_id) REFERENCES dim_produk(produk_id)
    );
""")
conn.commit()
print("Star schema berhasil dibuat")
conn.close()

conn = sqlite3.connect("fase_b/warehouse.db")

# Isi dimension tables
conn.executescript("""
    INSERT INTO dim_customer VALUES
        (1, 'Davis', 'Surabaya', 'Premium'),
        (2, 'Andi', 'Jakarta', 'Regular'),
        (3, 'Budi', 'Surabaya', 'Premium');
    
    INSERT INTO dim_produk VALUES
        (1, 'Laptop', 'Elektronik', 8000000),
        (2, 'Mouse', 'Elektronik', 150000),
        (3, 'Meja', 'Furniture', 1500000);
    
    INSERT INTO fact_transaksi VALUES
        (1, 1, 1, 1, 8000000, '2026-01-01'),
        (2, 1, 2, 2, 300000, '2026-01-02'),
        (3, 2, 1, 1, 8000000, '2026-01-03'),
        (4, 3, 3, 1, 1500000, '2026-01-04'),
        (5, 2, 2, 3, 450000, '2026-01-05');
""")

conn.commit()

# Query Star Schema
df = pd.read_sql("""
    SELECT 
        c.nama as customer,
        c.kategori,
        p.nama_produk as produk,
        p.kategori_produk,
        f.jumlah,
        f.total_nilai,
        f.tanggal
    FROM fact_transaksi f
    JOIN dim_customer c ON f.customer_id = c.customer_id
    JOIN dim_produk p ON f.produk_id = p.produk_id
    ORDER BY f.tanggal
""", conn)

print(df)
conn.close()