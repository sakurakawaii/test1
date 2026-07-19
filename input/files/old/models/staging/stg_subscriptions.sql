{{ config(materialized='view') }}

with source as (

    select * from {{ source('billing', 'subscriptions') }}

),

renamed as (

    select
        subscription_id,
        account_id,
        plan_tier,
        monthly_price_cents,
        seat_count,
        start_date,
        end_date,
        status,
        IFF(cancellation_reason is null and status = 'active', true, false)  as auto_renew_flag,
        created_at

    from source

)

select * from renamed
