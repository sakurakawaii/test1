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

currency_overrides as (

    select * from {{ ref('int_currency_rates') }}

),

joined as (

    select
        m.account_id,
        a.account_name,
        a.region,
        m.plan_tier,
        m.mrr_amount,
        ISNULL(m.mrr_amount * fx.rate_to_usd, 0)  as mrr_amount_usd,
        co.override_rate,
        m.status,
        RANK() OVER (ORDER BY m.mrr_amount DESC)  as mrr_rank,
        GETDATE()                                 as as_of_ts

    from mrr m
    inner join accounts a
        on m.account_id = a.account_id
    cross join fx
    left join currency_overrides co
        on m.account_id = co.account_id

)

select * from joined
