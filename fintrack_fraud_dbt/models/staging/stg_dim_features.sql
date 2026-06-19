with source as (
    select * from {{ source('fintrack_raw', 'dim_features') }}
)
select
    feature_name,
    low_max,
    medium_max
from source