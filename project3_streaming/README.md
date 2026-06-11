# Real-time Streaming Pipeline — E-Commerce Transactions

Pipeline streaming end-to-end yang mensimulasikan transaksi e-commerce secara real-time,
mengalirkan data melalui Kafka, dan menyimpannya ke PostgreSQL dengan monitoring otomatis.

---

## Arsitektur

```
[ Producer ]      ← producer.py
     │              Simulasi transaksi e-commerce setiap 1 detik
     │              order_id, customer_id, product, amount, payment_type
     ▼
[ Kafka ]
     │              Topic: transactions
     │              Message broker — simpan data sampai 7 hari
     ▼
[ Consumer ]      ← consumer.py
     │              Baca dari Kafka, simpan ke PostgreSQL
     │              Monitoring: stats per 10 transaksi
     │              Log ke file: logs/consumer.log
     ▼
[ PostgreSQL ]
                    Tabel: transactions
                    Storage permanen untuk analisis
```

---

## Tech Stack

| Layer           | Tools                        |
|-----------------|------------------------------|
| Bahasa          | Python 3.13                  |
| Message Broker  | Apache Kafka 3.7.0           |
| Storage         | PostgreSQL 15                |
| Containerization| Docker + Docker Compose      |
| Logging         | Python logging module        |
| Version control | Git + GitHub                 |

---

## Struktur Folder

```
de-learning-journey/
└── project3_streaming/
    ├── producer.py    # Generate & kirim transaksi ke Kafka
    └── consumer.py    # Baca dari Kafka, simpan ke PostgreSQL
└── logs/
    └── consumer.log   # Log file monitoring consumer
└── docker-compose.yml # Kafka + PostgreSQL
```

---

## Schema Tabel PostgreSQL

```sql
CREATE TABLE IF NOT EXISTS transactions (
    order_id      VARCHAR(20),
    customer_id   VARCHAR(20),
    product       VARCHAR(50),
    amount        NUMERIC(15,2),
    payment_type  VARCHAR(20),
    timestamp     TIMESTAMP,
    created_at    TIMESTAMP DEFAULT NOW()
);
```

---

## Cara Menjalankan

### 1. Clone repo

```bash
git clone https://github.com/Davisardo/de-learning-journey.git
cd de-learning-journey
```

### 2. Buat virtual environment

```bash
python -m venv venv
venv\Scripts\activate
pip install kafka-python psycopg2-binary
```

### 3. Jalankan Kafka dan PostgreSQL

```bash
docker compose up kafka postgres -d
```

### 4. Buat tabel di PostgreSQL

```bash
docker exec -it de-learning-journey-postgres-1 psql -U davis -d crypto_db
```

```sql
CREATE TABLE IF NOT EXISTS transactions (
    order_id VARCHAR(20),
    customer_id VARCHAR(20),
    product VARCHAR(50),
    amount NUMERIC(15,2),
    payment_type VARCHAR(20),
    timestamp TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);
```

Ketik `\q` untuk keluar.

### 5. Jalankan producer dan consumer

Terminal 1:
```bash
python project3_streaming/producer.py
```

Terminal 2:
```bash
python project3_streaming/consumer.py
```

### 6. Stop pipeline

Tekan `Ctrl+C` di kedua terminal. Consumer akan otomatis print summary akhir.

---

## Contoh Output Log

**Producer:**
```
2026-06-11 14:23:25 - INFO - Terkirim: {'order_id': 'ORD-65591', 'customer_id': 'CUST-405', 'product': 'laptop', 'amount': 3162544.83, 'payment_type': 'transfer'}
```

**Consumer:**
```
2026-06-11 14:23:24 - INFO - === Stats: 30 sukses | 0 error | 25 detik berjalan ===
2026-06-11 14:24:08 - INFO - === Consumer dihentikan ===
2026-06-11 14:24:08 - INFO - === Total: 74 sukses | 0 error | 69 detik ===
2026-06-11 14:24:08 - INFO - === Koneksi database ditutup ===
```

---

## Kenapa Streaming, Bukan Batch?

Pipeline ini dirancang untuk use case yang membutuhkan pemrosesan data **segera saat event terjadi** — bukan dikumpulkan dulu lalu diproses nanti.

Contoh use case nyata:
- Deteksi transaksi fraud sebelum disetujui
- Notifikasi order masuk ke seller secara real-time
- Monitoring inventory saat stok habis

Batch pipeline (Project 1 & 2) tidak cocok untuk ini karena latency-nya terlalu tinggi (menit hingga jam). Streaming memproses setiap event dalam hitungan milidetik.

---

## Keputusan Desain

**`auto_offset_reset='latest'`**
Consumer hanya baca message baru setelah dia nyala. Dipilih karena use case kita adalah monitoring real-time, bukan reprocessing data lama.

**Stats setiap 10 transaksi**
Monitoring tidak perlu terlalu sering (memberatkan log) tapi cukup informatif untuk deteksi masalah awal.

**`conn.rollback()` saat error**
Jika insert gagal, transaksi database di-rollback agar tidak ada data korup yang masuk ke PostgreSQL.

---

## Yang Bisa Dikembangkan

- Tambah dead letter queue — simpan transaksi yang gagal diproses ke tabel terpisah
- Deteksi anomali — alert kalau ada transaksi dengan amount di atas threshold
- Integrasi dengan Spark Streaming untuk pemrosesan paralel skala besar
- Deploy ke GCP dengan Pub/Sub sebagai pengganti Kafka