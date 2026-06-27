# Project 5 — RouteWise Logistics: Supply Chain Delivery Performance Pipeline

Pipeline data end-to-end untuk menganalisis performa pengiriman e-commerce di RouteWise Logistics. Dibangun menggunakan Python + Pandas untuk eksplorasi, cleaning, dan transformasi data; Google BigQuery sebagai cloud data warehouse; dbt untuk transformasi SQL dan automated testing; serta Looker Studio untuk dashboard yang siap dipakai tim Operations.

---

## Arsitektur Pipeline

```
DataCoSupplyChainDataset.csv (180.519 baris, 53 kolom)
        │
        ▼
explore.py ──► structural check, completeness check, distribution check,
        │       derive delay rate (57.28%) & delay rate per Shipping Mode
        ▼
clean.py ──► validate_and_clean(): drop duplicates, dropna kolom wajib,
        │    fill Order/Customer Zipcode → 'UNKNOWN', validate Days < 0
        ▼
transform.py ──► create_fact_shipments(): select, rename, derive delay_days & delay_category
        │        create_dim_carrier(): deduplicate 4 Shipping Mode unik
        │        create_dim_route(): deduplicate 39.107 kombinasi origin+destination
        ▼
load_bigquery.py ──► load_to_bigquery() dengan WRITE_TRUNCATE + verify baris
        │
        ▼
Google BigQuery (dataset: routewise_logistics)
  ├── fact_shipments   (180.519 baris)
  ├── dim_carrier      (4 baris)
  └── dim_route        (39.107 baris)
        │
        ▼
dbt (routewise_dbt)
  └── mart_carrier_performance ──► total_shipment, avg_delay_days, delay_rate per carrier
        │
        ▼
Looker Studio Dashboard
  ├── Scorecard: Total Shipment (180.519)
  ├── Scorecard: Avg Delay Rate (66.83%)
  ├── Bar Chart: Delay Rate per Carrier (%)
  └── Pie Chart: Breakdown Delay Category
```

---

## Desain Schema (Star Schema)

- **`fact_shipments`** (180.519 baris): tabel utama transaksi pengiriman — menyimpan `shipment_id`, `carrier`, `origin`, `destination`, `order_date`, `days_shipping_real`, `days_shipping_scheduled`, `delivery_status`, `late_delivery_risk`, plus kolom turunan `actual_delivery_date`, `expected_delivery_date`, `delay_days`, `delay_category`
- **`dim_carrier`** (4 baris): daftar 4 Shipping Mode unik — Standard Class, First Class, Second Class, Same Day — dengan `carrier_id` sebagai primary key
- **`dim_route`** (39.107 baris): daftar kombinasi unik `origin` (Order City) + `destination` (Customer City) dengan `route_id` sebagai primary key

---

## Tech Stack

| Layer | Tools |
|---|---|
| Bahasa | Python 3.13 + Pandas |
| Cloud Warehouse | Google BigQuery |
| Transformasi SQL | dbt 1.11.11 + dbt-bigquery 1.11.1 |
| Visualisasi | Looker Studio |
| IDE | VS Code |
| Version Control | Git + GitHub |

---

## Struktur Folder

```
de-learning-journey/
└── project5_routewise-logistics/
    ├── data/
    │   └── DataCoSupplyChainDataset.csv
    ├── explore.py
    ├── clean.py
    ├── transform.py
    ├── load_bigquery.py
    └── routewise_dbt/
        ├── models/
        │   ├── marts/
        │   │   ├── mart_carrier_performance.sql
        │   │   └── schema.yml
        │   └── staging/
        │       └── sources.yml
        └── dbt_project.yml
```

> `profiles.yml` disimpan global di `~/.dbt/profiles.yml`, bukan di dalam folder project.

---

## Keputusan Penting Engineering

1. **Derive `expected_delivery_date` dari kolom numerik:** Dataset tidak punya kolom tanggal ekspektasi secara langsung. Kolom ini di-derive menggunakan `order_date + pd.to_timedelta(days_shipping_scheduled, unit='D')` — lebih realistis dengan kondisi data dunia kerja yang jarang sempurna.
2. **Fill `UNKNOWN` untuk Zipcode, bukan di-drop:** `Order Zipcode` kosong 86.24% dan `Customer Zipcode` kosong 0.001%. Keputusan fill dengan string `'UNKNOWN'` karena kolom ini bukan kolom kunci analisis delay — membuang baris karena zipcode kosong berarti kehilangan 86% data tanpa alasan bisnis yang valid.
3. **WRITE_TRUNCATE untuk semua tabel:** Dataset ini bersifat historical (2015–2018), bukan streaming real-time. Tidak ada risiko kehilangan data baru karena tidak ada data baru yang masuk setiap hari. WRITE_TRUNCATE menjamin pipeline idempotent — aman dijalankan berkali-kali tanpa duplikat.
4. **Verify setelah load:** Setiap load ke BigQuery diikuti langkah verify menggunakan `client.get_table(table_id).num_rows` — membandingkan baris yang dikirim dari Python dengan baris yang benar-benar tersimpan di BigQuery. Hasil: fact_shipments 180.519 = 180.519, dim_carrier 4 = 4, dim_route 39.107 = 39.107.
5. **`delay_category` tiga tingkat, bukan binary:** Kategorisasi On Time (≤0 hari), Slight Delay (1–3 hari), Major Delay (>3 hari) jauh lebih actionable untuk tim Ops daripada sekadar "telat atau tidak". Dari hasil dashboard: 53.4% Slight Delay, 42.7% On Time, 3.9% Major Delay.
6. **Cross-check delay rate dari dua sumber:** `Delivery Status` dari sistem melaporkan 54.8% Late delivery, tapi hasil perhitungan kita dari kolom tanggal menghasilkan 57.28%. Selisih 2.48% = sekitar 4.480 shipment yang statusnya tidak konsisten antara label sistem vs perhitungan aktual — di-flag sebagai temuan Data Quality.
7. **First Class 100% delay di-flag sebagai anomali:** Angka tepat 100% pada 27.814 order mencurigakan secara statistik. Di-flag untuk investigasi lebih lanjut ke tim Data Quality sebelum dipakai sebagai dasar keputusan operasional.

---

## Cara Menjalankan Pipeline

### 1. Clone repo & setup environment
```bash
git clone https://github.com/Davisardo/de-learning-journey.git
cd de-learning-journey/project5_routewise-logistics
pip install -r ../requirements.txt
```

### 2. Download dataset
Download dari Kaggle: [DataCo SMART SUPPLY CHAIN FOR BIG DATA ANALYSIS](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis)

Taruh file di:
```
project5_routewise-logistics/data/DataCoSupplyChainDataset.csv
```

### 3. Eksplorasi data
```bash
python explore.py
```
Output: shape, missing values (%), distribution Delivery Status & Shipping Mode, overall delay rate, delay rate per Shipping Mode.

### 4. Validasi & cleaning
```bash
python clean.py
```
Output log: baris awal, duplikat dibuang, missing kolom wajib dibuang, kolom opsional di-fill, baris akhir, % data tersisa.

### 5. Transformasi ke fact & dimension table
```bash
python transform.py
```
Output: `fact_shipments` (180.519 baris), `dim_carrier` (4 baris), `dim_route` (39.107 baris).

### 6. Load ke BigQuery
Pastikan sudah setup Google Cloud credentials dan dataset `routewise_logistics` sudah dibuat di BigQuery (region: us-central1).
```bash
python load_bigquery.py
```
Output log: jumlah baris dikirim + jumlah baris terverifikasi di BigQuery untuk setiap tabel.

### 7. Jalankan dbt
```bash
cd routewise_dbt
set PYTHONUTF8=1
dbt run
dbt test
```

### 8. Dashboard
Buka [Looker Studio](https://lookerstudio.google.com), connect ke `amplified-ward-416314.routewise_logistics.mart_carrier_performance` dan `fact_shipments`, lalu buat:
- 2 Scorecard (Total Shipment & Avg Delay Rate)
- 1 Bar Chart (Delay Rate per Carrier)
- 1 Pie Chart (Breakdown Delay Category)

---

## Hasil dbt Test

| Test | Kolom | Model | Status |
|---|---|---|---|
| not_null | carrier | mart_carrier_performance | ✅ PASS |
| not_null | total_shipment | mart_carrier_performance | ✅ PASS |
| not_null | delay_rate | mart_carrier_performance | ✅ PASS |
| unique | carrier | mart_carrier_performance | ✅ PASS |

**Total: 4/4 PASS**