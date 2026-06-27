# FinTrack: Credit Card Fraud Detection Data Pipeline

## Deskripsi Proyek

FinTrack memproses ratusan ribu transaksi kartu kredit setiap harinya. Proyek ini membangun data pipeline end-to-end berbasis *star schema* untuk membantu tim *fraud analyst* mendeteksi pola transaksi mencurigakan. Pipeline memproses data mentah CSV, melakukan validasi kualitas data, memodelkan dimensi bisnis di BigQuery, mentransformasi dengan dbt, hingga menyajikan metrik *fraud rate* siap pakai pada dashboard Looker Studio.

---

## Arsitektur Pipeline

```
CSV Mentah (creditcard.csv)
        │
        ▼
validate.py ──► Cek missing values, duplikat, range Amount & Time
        │
        ▼
transform.py ──► Star Schema (1 Fact + 4 Dim tables) via Pandas
        │
        ▼
load_to_bq.py ──► Incremental Load ke Google BigQuery
        │
        ▼
dbt (staging → mart) ──► SQL transform + 4 jenis automated test
        │
        ▼
Looker Studio Dashboard ──► Fraud rate, tren per jam, breakdown per kategori
```

---

## Desain Schema (Star Schema)

- **`fact_transactions`**: Menyimpan semua metrik utama transaksi beserta foreign keys ke tabel dimensi.
- **`dim_time`**: Mentransformasi waktu (detik) menjadi jam operasional (0-23), periode waktu (Night/Morning/Afternoon/Evening), dan penanda jam sibuk (`is_peak_hour`).
- **`dim_amount`**: Mengelompokkan nominal transaksi ke bucket logis (Small, Medium, Large, Very Large) berdasarkan distribusi data aktual.
- **`dim_fraud`**: Menyediakan label status fraud dan tingkat risiko terkait (Normal/Low, Fraud/High).
- **`dim_features`**: Menyimpan batas kategori komponen PCA (V1-V3) untuk kebutuhan analisis lanjutan.

---

## Tech Stack

| Layer | Tools |
|---|---|
| Ingestion & Transform | Python, Pandas |
| Data Quality | Python Logging |
| Data Warehouse | Google BigQuery |
| SQL Transform & Testing | dbt |
| Visualisasi | Looker Studio |
| Version Control | Git + GitHub |

---

## Struktur Folder

```
de-learning-journey/
└── project4_fintrack_fraud/
    ├── data/
    │   └── creditcard.csv
    ├── explore.py        # Eksplorasi awal dataset
    ├── validate.py        # Data quality & validasi
    ├── transform.py       # Star schema via Pandas
    ├── load_to_bq.py       # Incremental load ke BigQuery
    └── fintrack_dbt/
        ├── models/
        │   ├── staging/
        │   └── marts/
        │       └── mart_fraud_analysis.sql
        └── dbt_project.yml
```

> `profiles.yml` disimpan global di `~/.dbt/profiles.yml`, bukan di dalam folder project.

---

## Keputusan Penting Engineering

1. **Integritas Data Fraud (Amount = $0):** Ditemukan 1.825 transaksi bernilai $0. Data ini **tidak dihapus** karena terdeteksi 27 kasus fraud nyata di dalamnya (pola *card-testing* — fraudster memvalidasi kartu curian dengan transaksi $0 sebelum melakukan transaksi besar). Membuang data ini berarti kehilangan sinyal fraud penting.
2. **Pembersihan Duplikat:** Sebanyak 1.081 baris duplikat di-drop untuk menjaga integritas metrik agregasi. Tanpa penghapusan ini, fraud count akan terhitung ganda dan fraud rate menjadi tidak akurat.
3. **Incremental Load (bukan WRITE_TRUNCATE):** Data di-load secara inkremental ke BigQuery menggunakan checkpoint `MAX(transaction_id)`. Ini menjaga data historis tetap aman saat pipeline dijalankan ulang setiap hari, sekaligus menghemat biaya BigQuery karena hanya baris baru yang ditulis.
4. **Data-Driven Peak Hours:** Penentuan `is_peak_hour` dilakukan secara dinamis berdasarkan top 25% volume transaksi aktual dari data (Jam 21, 18, 11, 20, 10, 14) — bukan asumsi manual. Ini penting karena kolom `Time` di dataset adalah detik relatif tanpa konteks tanggal/waktu nyata.
5. **Staging & Mart Layer di dbt:** Staging layer (`stg_*`) berfungsi sebagai satu pintu masuk per source table dengan tugas menyeragamkan nama kolom. Mart layer (`mart_fraud_analysis`) menggabungkan semua staging table menjadi satu output siap pakai untuk dashboard — analyst tidak perlu tulis JOIN sendiri.

---

## Cara Menjalankan Pipeline

### 1. Clone repo & setup environment
```bash
git clone https://github.com/Davisardo/de-learning-journey.git
cd de-learning-journey/project4_fintrack_fraud
pip install -r ../requirements.txt
```

### 2. Download dataset
Download dari [Kaggle — Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud), simpan ke folder `data/` di dalam `project4_fintrack_fraud/`:
```
project4_fintrack_fraud/data/
└── creditcard.csv
```

### 3. Data Quality & Validasi
```bash
python validate.py
```

### 4. Transformasi Data & Pembentukan Schema
```bash
python transform.py
```

### 5. Load ke BigQuery (Incremental)
```bash
python load_to_bq.py
```

### 6. dbt Transform & Testing
```bash
cd fintrack_dbt
dbt run
dbt test
```

### 7. Dashboard
Buka Looker Studio → connect ke `mart_fraud_analysis` di dataset `fintrack_fraud`.

---

## Hasil dbt Test

| Test | Model | Status |
|---|---|---|
| not_null | transaction_id, amount, fraud_label, time_period, amount_bucket | PASS |
| unique | transaction_id | PASS |
| accepted_values | fraud_label (Normal/Fraud) | PASS |
| accepted_values | amount_bucket (Small/Medium/Large/Very Large) | PASS |
| accepted_values | time_period (Morning/Afternoon/Evening/Night) | PASS |
| relationships | amount_bucket → dim_amount | PASS |
| relationships | fraud_class → dim_fraud | PASS |

**Total: 13/13 PASS**