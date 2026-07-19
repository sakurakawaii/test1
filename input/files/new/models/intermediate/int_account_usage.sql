{{ config(materialized='table') }}

with usage as (

    select * from {{ ref('stg_usage_events') }}

),

deduped_sessions as (

    select distinct
        account_id,
        org_id,
        event_id
    from usage

),

account_flags as (

    select
        account_id,
        ARRAY_AGG(DISTINCT event_type)                              as event_type_array

    from usage
    group by account_id

),

final as (

    select
        account_id,
        event_type_array,
        ARRAY_CONTAINS('sso_login', event_type_array)               as has_sso_login,
        {{ first_touch_feature('event_type_array') }}               as first_event_type

    from account_flags

)

select * from final
