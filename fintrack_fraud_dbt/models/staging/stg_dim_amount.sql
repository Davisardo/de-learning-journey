with source as (
    select * from {{ source('fintrack_raw', 'dim_amount') }}
)
select
    amount_bucket,
    min_range,
    max_range
from source