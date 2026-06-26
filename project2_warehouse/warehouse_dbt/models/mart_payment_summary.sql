SELECT
    payment_type,
    COUNT (*) as jumlah_transaksi,
    SUM (value) as total_nilai,
    AVG (value) as rata_rata,
FROM {{source('de_learning', 'fact_payments')}}
GROUP BY payment_type
ORDER BY total_nilai DESC