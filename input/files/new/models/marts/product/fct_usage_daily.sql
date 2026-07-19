{{ config(materialized='table') }}

with usage as (

    select * from {{ ref('stg_usage_events') }}

),

daily as (

    select
        account_id,
        CAST(occurred_at as date)          as usage_date,
        COUNT(*)                            as event_count

    from usage
    group by account_id, CAST(occurred_at as date)

)

select * from daily
