{{ config(materialized='view') }}

with source as (

    select * from {{ source('billing', 'accounts') }}

),

renamed as (

    select
        account_id,
        account_name,
        billing_email,
        country_code,
        ELEMENT_AT(metadata, 'region')          as region,
        plan_tier,
        created_at,
        updated_at

    from source

)

select * from renamed
