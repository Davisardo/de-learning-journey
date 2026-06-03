-- Model dbt: transaksi_summary
-- Agregasi dari model transaksi_clean

SELECT
    status,
    COUNT(*) as jumlah,
    SUM(nilai_transaksi) as total_nilai,
    AVG(nilai_transaksi) as rata_rata
FROM {{ ref ('transaksi_clean')}}
GROUP BY status