{{ config(materialized='table') }}

with accounts as (

    select * from {{ ref('stg_accounts') }}

),

final as (

    select
        {{ generate_surrogate_key(['account_id']) }}    as account_sk,
        account_id,
        account_name,
        billing_email,
        country_code,
        region,
        plan_tier,
        created_at
    from accounts

)

select * from final
