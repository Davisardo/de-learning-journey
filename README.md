# Crypto ETL Pipeline

Pipeline data end-to-end yang mengambil data harga cryptocurrency secara otomatis,
membersihkan dan mentransformasinya, lalu menyimpannya ke database PostgreSQL
untuk divisualisasikan via Metabase.

---

## Arsitektur

CoinGecko API
│
▼
[ Extract ]  ← extract.py
│         Ambil top 10 crypto (harga, market cap, volume)
▼
[ Transform ] ← transform.py
│         Bersihkan data, tambah kolom trend & processed_at
▼
[ Load ]     ← load.py
│         Simpan ke PostgreSQL (tabel crypto_prices)
▼
[ Dashboard ] ← Metabase
Visualisasi harga & trend per coin

---

## Tech Stack

| Layer        | Tools                  |
|--------------|------------------------|
| Bahasa       | Python 3.13            |
| Data source  | CoinGecko API (free)   |
| Transform    | Pandas                 |
| Database     | PostgreSQL (Docker)    |
| Dashboard    | Metabase (Docker)      |
| Logging      | Python logging module  |
| Version control | Git + GitHub        |

---

## Struktur Folder

de-learning-journey/
└── crypto_pipeline/
├── extract.py      # Ambil data dari CoinGecko API
├── transform.py    # Bersihkan dan transformasi data
├── load.py         # Load ke PostgreSQL
└── pipeline.py     # Entry point — jalankan ETL end-to-end

---

## Cara Menjalankan

### 1. Clone repo
```bash
git clone https://github.com/<username>/de-learning-journey.git
cd de-learning-journey
```

### 2. Buat virtual environment
```bash
python -m venv venv
venv\Scripts\activate
pip install requests pandas psycopg2-binary
```

### 3. Jalankan PostgreSQL via Docker
```bash
docker run --name crypto-postgres \
  -e POSTGRES_USER=davis \
  -e POSTGRES_PASSWORD=davis123 \
  -e POSTGRES_DB=crypto_db \
  -p 5432:5432 -d postgres
```

### 4. Jalankan pipeline
```bash
python crypto_pipeline/pipeline.py
```

### 5. Lihat dashboard
Buka Metabase di `http://localhost:3000` — connect ke PostgreSQL lalu buat visualisasi dari tabel `crypto_prices`.

---

## Contoh Output Log

2026-06-08 00:13:44 - INFO - === Crypto ETL Pipeline Dimulai ===
2026-06-08 00:13:45 - INFO - Berhasil ambil 10 data crypto
2026-06-08 00:13:45 - INFO - Transform selesai: 10 baris
2026-06-08 00:13:46 - INFO - Tabel crypto_prices siap
2026-06-08 00:13:46 - INFO - Berhasil load 10 baris ke PostgreSQL
2026-06-08 00:13:46 - INFO - === Pipeline Selesai ===

---

## Yang Bisa Dikembangkan

- Tambah scheduling dengan Apache Airflow
- Simpan data historis untuk analisis trend jangka panjang
- Integrasi dengan Power BI untuk enterprise reporting
- Deploy ke cloud (GCP / AWS)