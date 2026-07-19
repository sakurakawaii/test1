{{ config(materialized='table') }}

with accounts as (

    select * from {{ ref('stg_accounts') }}

),

mrr as (

    select * from {{ ref('int_subscription_mrr') }}

),

health as (

    select
        a.account_id,
        a.account_name,
        a.region,
        m.status = 'active'                  as is_currently_active,
        m.mrr_amount,
        m.seat_count

    from accounts a
    left join mrr m
        on a.account_id = m.account_id

)

select * from health
