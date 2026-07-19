{{ config(materialized='table') }}

with health as (

    select * from {{ ref('int_account_health') }}

),

trial_conversions as (

    select * from {{ ref('int_trial_conversion') }}

),

churned as (

    select
        h.account_id,
        h.account_name,
        h.is_active,
        h.mrr_amount,
        h.seat_count,
        t.converted_at
    from health h
    left join trial_conversions t
        on h.account_id = t.account_id
    where h.is_active = false

)

select * from churned
