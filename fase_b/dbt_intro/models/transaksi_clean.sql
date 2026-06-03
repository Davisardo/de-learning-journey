-- Model dbt: transaksi_clean
-- Transformasi data transaksi mentah

SELECT
    user_id,
    nama,
    nilai_transaksi,
    CASE
        WHEN nilai_transaksi > 0 THEN 'VALID'
        WHEN nilai_transaksi = 0 THEN ' PERLU DICEK'
        ELSE 'INVALID'
    END as status,
    CURRENT_TIMESTAMP as processed_at
FROM transaksi
WHERE user_id IS NOT NULL