# Data Engineering Learning Journey

Dokumentasi perjalanan belajar Data Engineering secara mandiri — dari fondasi Python hingga membangun pipeline data end-to-end yang merepresentasikan workflow nyata seorang Data Engineer.

---

## Tentang Repo Ini

Repo ini berisi progres belajar terstruktur, dibagi menjadi beberapa fase:

- **Fase A & B** — latihan fondasi Python, Pandas, SQL, dan konsep dasar data engineering
- **Project 1–5** — project end-to-end yang meniru skenario kerja nyata, dari ETL sederhana hingga real-time streaming dan data warehouse dengan dbt

Setiap project dibangun dengan tools yang umum dipakai industri: Python, Docker, BigQuery, dbt, Apache Kafka, dan PostgreSQL.

---

## Daftar Project

| Project | Nama | Domain | Stack Utama |
|---|---|---|---|
| 1 | [Crypto ETL Pipeline](./project1_crypto_pipeline) | Cryptocurrency | Python, PostgreSQL, Docker, Metabase |
| 2 | [Mini Data Warehouse](./project2_warehouse) | E-Commerce (Olist) | Python, BigQuery, dbt, Looker Studio |
| 3 | [Real-time Streaming Pipeline](./project3_streaming) | E-Commerce (simulasi) | Apache Kafka, Python, PostgreSQL |
| 4 | [FinTrack Fraud Detection](./project4_fintrack_fraud) | Fintech | Python, BigQuery, dbt (incremental load + staging) |
| 5 | [RouteWise Logistics](./project5_routewise-logistics) | Logistik/Supply Chain | Python, BigQuery, dbt |

Setiap folder project punya README sendiri yang menjelaskan arsitektur, cara menjalankan, dan keputusan desain secara detail.

---

## Progres Pembelajaran

**Project 1 — Crypto ETL Pipeline**
Pipeline ETL batch dasar: ambil data harga crypto dari API publik, transformasi dengan Pandas, simpan ke PostgreSQL, visualisasi di Metabase. Fokus: idempotent pipeline, logging, containerization.

**Project 2 — Mini Data Warehouse**
Star schema (1 fact + 3 dimension table) dari dataset e-commerce Olist Brazil, di-load ke BigQuery, ditransformasi dengan dbt, divisualisasikan di Looker Studio. Fokus: data modeling, dbt testing, data quality.

**Project 3 — Real-time Streaming Pipeline**
Simulasi transaksi e-commerce yang dialirkan via Apache Kafka (producer-consumer pattern), disimpan ke PostgreSQL dengan monitoring otomatis. Fokus: batch vs streaming, message broker, credentials management.

**Project 4 — FinTrack Fraud Detection**
Data warehouse fintech dengan kompleksitas production-like: incremental load (bukan full overwrite), staging layer di dbt, data quality validation terpisah, dan dashboard fraud analyst. Fokus: pola kerja Data Engineer di industri nyata.

**Project 5 — RouteWise Logistics**
Pipeline performa pengiriman logistik, dirancang sebagai quest 6 level dengan pendekatan "Code Blueprint" — setiap jenis file (eksplorasi, cleaning, transformasi, loading, dbt, dashboard) punya pola standar yang bisa dipakai berulang di project manapun. Fokus: membangun template berpikir Data Engineer, bukan sekadar menyelesaikan tugas.

---

## Tech Stack

| Kategori | Tools |
|---|---|
| Bahasa | Python 3.13 |
| Data Warehouse | Google BigQuery |
| Transformasi | dbt (data build tool) |
| Streaming | Apache Kafka |
| Database | PostgreSQL |
| Visualisasi | Looker Studio, Metabase |
| Containerization | Docker, Docker Compose |
| Version Control | Git, GitHub |

---

## Struktur Repo

```
de-learning-journey/
├── fase_a/                       # Latihan fondasi Python
├── fase_b/                       # Latihan SQL, dbt intro, konsep ETL
├── project1_crypto_pipeline/
├── project2_warehouse/
│   └── warehouse_dbt/
├── project3_streaming/
├── project4_fintrack_fraud/
│   └── fintrack_dbt/
├── project5_routewise-logistics/
│   └── routewise_dbt/
├── docker-compose.yml             # Kafka, PostgreSQL, Metabase
├── requirements.txt
└── README.md
```

---

## Catatan

Dataset mentah (CSV) tidak disertakan di repo ini — sesuai praktik standar, raw data tidak disimpan di version control. Setiap README project menyertakan link sumber dataset (Kaggle) dan instruksi penempatannya.

Credentials (`.env`, API keys) juga tidak disertakan — lihat README masing-masing project untuk environment variable yang dibutuhkan.
