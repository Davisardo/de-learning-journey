SELECT
    carrier,
    COUNT(shipment_id) as total_shipment,
    ROUND(AVG(delay_days),2) as avg_delay_days,
    ROUND(AVG(CASE WHEN delay_days > 0 THEN 1 ELSE 0 END)*100, 2) as delay_rate 

FROM {{ source('routewise_logistics', 'fact_shipments') }}

GROUP BY carrier 
ORDER BY delay_rate DESC