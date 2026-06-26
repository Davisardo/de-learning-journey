with fact as (
    select * from {{ ref('stg_fact_transactions') }}
)

select
    fact.transaction_id,
    fact.hour,
    fact.amount,
    fact.v1_category,
    fact.v2_category,
    fact.v3_category,
    time.time_period,
    time.is_peak_hour,
    amt.amount_bucket,
    fraud.fraud_label,
    fraud.risk_level
from fact
left join {{ ref('stg_dim_time') }} as time on fact.hour = time.hour
left join {{ ref('stg_dim_amount') }} as amt on fact.amount_bucket = amt.amount_bucket
left join {{ ref('stg_dim_fraud') }} as fraud on fact.fraud_class = fraud.fraud_class