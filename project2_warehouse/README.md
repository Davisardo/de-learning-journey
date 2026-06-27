# Mini Data Warehouse — Olist Brazil E-Commerce

Pipeline data warehouse end-to-end yang mengambil data e-commerce publik (Olist Brazil),
membersihkan dan mentransformasinya menggunakan Python, memuatnya ke Google BigQuery,
mentransformasikan dengan dbt, dan memvisualisasikan hasilnya di Looker Studio.

---

## Arsitektur

```
CSV Files (Kaggle)
     │
     ▼
[ Transform ]  ← transform.py
     │           Baca 4 CSV, buat fact & dimension tables
     │           Filter data tidak valid (not_defined)
     ▼
[ Load ]       ← load_bigquery.py
     │           Upload ke Google BigQuery (WRITE_TRUNCATE)
     │           4 tabel: dim_orders, fact_payments,
     │                    dim_customers, dim_products
     ▼
[ Transform ]  ← dbt (warehouse_dbt)
     │           mart_payment_summary — agregasi per payment type
     │           4 data tests: not_null & unique
     ▼
[ Dashboard ]  ← Looker Studio
                 Visualisasi total nilai transaksi per payment type
```

---

## Tech Stack

| Layer           | Tools                        |
|-----------------|-------------------------------|
| Bahasa          | Python 3.13                  |
| Data source     | Kaggle — Olist Brazil Dataset |
| Transform       | Pandas                       |
| Data Warehouse  | Google BigQuery (free tier)  |
| dbt             | dbt-bigquery 1.11.1          |
| Dashboard       | Looker Studio                |
| Logging         | Python logging module        |
| Version control | Git + GitHub                 |

---

## Schema Design (Star Schema)

```
                  dim_orders
                  (order_id PK)
                       │
dim_customers ─── fact_payments ─── dim_products
(customer_id PK)  (order_id FK)     (product_id PK)
```

### Tabel

| Tabel | Tipe | Kolom Utama | Jumlah Baris |
|---|---|---|---|
| fact_payments | Fact | order_id, payment_type, installments, value | 103.883 |
| dim_orders | Dimension | order_id, customer_id, status, purchase_date | 99.441 |
| dim_customers | Dimension | customer_id, customer_city, customer_state | 99.441 |
| dim_products | Dimension | product_id, category_name, weight_g, length_cm | 32.951 |

---

## Struktur Folder

```
de-learning-journey/
└── project2_warehouse/
    ├── data/
    │   ├── olist_orders_dataset.csv
    │   ├── olist_order_payments_dataset.csv
    │   ├── olist_customers_dataset.csv
    │   └── olist_products_dataset.csv
    ├── transform.py       # Baca CSV, buat fact & dimension tables
    ├── load_bigquery.py   # Upload tabel ke Google BigQuery
    └── warehouse_dbt/
        ├── models/
        │   ├── mart_payment_summary.sql  # Agregasi per payment type
        │   └── schema.yml                # Sources & data tests
        └── dbt_project.yml
```

> `profiles.yml` disimpan global di `~/.dbt/profiles.yml`, bukan di dalam folder project.

---

## Cara Menjalankan

### 1. Clone repo
```bash
git clone https://github.com/Davisardo/de-learning-journey.git
cd de-learning-journey/project2_warehouse
```

### 2. Buat virtual environment
```bash
python -m venv venv
venv\Scripts\activate
pip install pandas google-cloud-bigquery db-dtypes dbt-bigquery
```

### 3. Download dataset
Download dari [Kaggle — Olist Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), simpan ke folder `data/` di dalam `project2_warehouse/`:
```
project2_warehouse/data/
├── olist_orders_dataset.csv
├── olist_order_payments_dataset.csv
├── olist_customers_dataset.csv
└── olist_products_dataset.csv
```

### 4. Setup autentikasi Google Cloud
```bash
gcloud auth application-default login
```

### 5. Jalankan pipeline ingestion
```bash
python load_bigquery.py
```

### 6. Jalankan dbt
```bash
cd warehouse_dbt
dbt run
dbt test
```

### 7. Lihat dashboard
Buka [Looker Studio](https://lookerstudio.google.com) → connect ke BigQuery → pilih tabel `mart_payment_summary`.

---

## Contoh Output Log

```
2026-06-09 21:21:56 - INFO - Load ke BigQuery dimulai
2026-06-09 21:21:57 - INFO - Orders: 99441 baris
2026-06-09 21:21:57 - INFO - Payments: 103886 baris
2026-06-09 21:21:57 - INFO - Customers: 99441 baris
2026-06-09 21:21:57 - INFO - Products: 32951 baris
2026-06-09 21:21:58 - INFO - dim_orders: 99441 baris
2026-06-09 21:21:58 - INFO - fact_payments: 103883 baris
2026-06-09 21:21:58 - INFO - dim_customers: 99441 baris
2026-06-09 21:21:58 - INFO - dim_products: 32951 baris
2026-06-09 21:22:38 - INFO - Loaded 99441 baris ke amplified-ward-416314.de_learning.dim_orders
2026-06-09 21:22:38 - INFO - Loaded 103883 baris ke amplified-ward-416314.de_learning.fact_payments
2026-06-09 21:22:38 - INFO - Loaded 99441 baris ke amplified-ward-416314.de_learning.dim_customers
2026-06-09 21:22:38 - INFO - Loaded 32951 baris ke amplified-ward-416314.de_learning.dim_products
2026-06-09 21:22:38 - INFO - Selesai
```

```
06:50:59  Found 1 model, 4 sources, 549 macros
06:50:59  1 of 1 OK created sql view model de_learning.mart_payment_summary
06:52:54  Done. PASS=4 WARN=0 ERROR=0 SKIP=0 TOTAL=4
```

---

## Keputusan Desain

**Filter `not_defined`**
Ditemukan 3 baris dengan `payment_type = "not_defined"` dan `value = 0.0`.
Diputuskan untuk difilter karena data tanpa nilai transaksi tidak memiliki makna bisnis.
Data yang masuk warehouse harus punya konteks yang jelas.

**WRITE_TRUNCATE di BigQuery**
Setiap run pipeline menghapus dan mengisi ulang tabel (idempotent).
Pipeline aman dijalankan berkali-kali tanpa menghasilkan duplikat.

**Separation of Concerns**
Ingestion (Python) dipisah dari transformasi (dbt).
Python bertanggung jawab memindahkan data, dbt bertanggung jawab mengolahnya.

---

## Yang Bisa Dikembangkan

- Tambah scheduling dengan Apache Airflow
- Tambah dimension tabel `dim_date` untuk analisis time series
- Incremental load — hanya proses data baru, bukan full refresh
- Deploy pipeline ke cloud (GCP Cloud Run / Cloud Composer)
- Tambah lebih banyak dbt models untuk insight bisnis lainnya