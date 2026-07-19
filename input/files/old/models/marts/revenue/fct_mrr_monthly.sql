{{ config(materialized='table') }}

with mrr as (

    select * from {{ ref('int_subscription_mrr') }}

),

accounts as (

    select * from {{ ref('dim_accounts') }}

),

fx as (

    select * from raw_billing.fx_rates
    where currency_code = 'USD'

),

joined as (

    select
        m.account_id,
        a.account_name,
        a.region,
        m.plan_tier,
        m.mrr_amount,
        m.mrr_amount * fx.rate_to_usd            as mrr_amount_usd,
        m.status,
        RANK()                                    as mrr_rank,
        GETDATE()                                 as as_of_ts

    from mrr m
    inner join accounts a
        on m.account_id = a.account_id
    cross join fx

)

select * from joined
