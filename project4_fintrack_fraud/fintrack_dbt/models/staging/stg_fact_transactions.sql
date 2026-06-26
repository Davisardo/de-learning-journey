with source as (
    select * from {{ source('fintrack_raw','fact_transactions' )}}
)

select
    transaction_id,
    hour,
    amount_bucket,
    Class as fraud_class,
    Amount as amount,
    V1_category as v1_category,
    V2_category as v2_category,
    V3_category as v3_category,
from source