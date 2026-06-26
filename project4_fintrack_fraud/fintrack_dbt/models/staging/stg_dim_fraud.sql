with source as (
    select * from {{ source('fintrack_raw', 'dim_fraud') }}
)
select
    Class as fraud_class,
    fraud_label,
    risk_level
from source