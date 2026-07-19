{{ config(materialized='view') }}

with source as (

    select * from {{ source('billing', 'invoices') }}

),

renamed as (

    select
        invoice_id,
        account_id,
        subscription_id,
        amount_due_cents / 100.0                as amount_due,
        invoice_date,
        DATE_FORMAT(invoice_date, 'yyyy-MM')    as invoice_month,
        due_date,
        paid_at,
        status

    from source

)

select * from renamed
