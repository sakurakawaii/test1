{{ config(materialized='view') }}

with source as (

    select * from {{ source('product', 'usage_events') }}

),

renamed as (

    select
        event_id,
        org_id,
        account_id,
        event_type,
        feature_keys,
        SIZE(feature_keys)                        as features_touched_count,
        LEN(event_type)                            as event_type_length,
        occurred_at

    from source

)

select * from renamed
