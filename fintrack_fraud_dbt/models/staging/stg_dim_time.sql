with source as (
    select * from {{ source('fintrack_raw', 'dim_time') }}
)

select
    hour,
    time_period,
    is_peak_hour
from source