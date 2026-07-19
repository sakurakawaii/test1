{{ config(materialized='view') }}

with source as (

    select * from {{ source('product', 'feature_flags') }}

),

renamed as (

    select
        flag_id,
        account_id,
        flag_name,
        SIZE(rollout_segments)                    as rollout_segment_count,
        {{ first_touch_feature('rollout_segments') }}   as first_segment,
        is_enabled,
        updated_at

    from source

)

select * from renamed
