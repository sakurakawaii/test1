{{ config(materialized='table') }}

with flags as (

    select * from {{ ref('stg_feature_flags') }}

),

final as (

    select
        flag_id,
        flag_name,
        is_enabled
    from flags

)

select * from final
