{{ config(materialized='table') }}

with subscriptions as (

    select * from {{ ref('stg_subscriptions') }}

),

mrr as (

    select
        subscription_id,
        account_id,
        plan_tier,
        seat_count,
        start_date,
        end_date,
        status,
        monthly_price_cents / 100.0
            * CASE
                WHEN DATE_CMP(DATE_TRUNC('month', start_date), DATE_TRUNC('month', CURRENT_DATE())) = 0
                    THEN DATEDIFF(day, start_date, DATEADD(month, 1, DATE_TRUNC('month', start_date))) / 30.0
                ELSE 1
              END                                                        as mrr_amount

    from subscriptions

)

select * from mrr
