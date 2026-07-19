{{ config(materialized='table') }}

with usage as (

    select * from {{ ref('stg_usage_events') }}

),

flags as (

    select * from {{ ref('stg_feature_flags') }}

),

adoption as (

    select
        u.account_id,
        f.flag_name,
        COUNT(DISTINCT u.event_id)          as usage_event_count,
        MAX(u.occurred_at)                  as last_used_at

    from usage u
    join flags f
        on u.account_id = f.account_id
    group by u.account_id, f.flag_name

)

select * from adoption
