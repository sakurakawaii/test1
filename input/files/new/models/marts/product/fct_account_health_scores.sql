{{ config(materialized='table') }}

with health as (

    select * from {{ ref('int_account_health') }}

),

scored as (

    select
        account_id,
        account_name,
        mrr_amount,
        seat_count,
        CASE
            WHEN mrr_amount >= 1000 THEN 'high'
            WHEN mrr_amount >= 200  THEN 'medium'
            ELSE 'low'
        END                                     as health_tier
    from health

)

select * from scored
