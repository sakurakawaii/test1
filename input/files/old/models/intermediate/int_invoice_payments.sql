{{ config(materialized='table') }}

with invoices as (

    select * from {{ ref('stg_invoices') }}

),

payment_status as (

    select
        invoice_id,
        account_id,
        amount_due,
        invoice_date,
        due_date,
        paid_at,
        status,
        CASE WHEN paid_at is not null THEN DATEDIFF(day, due_date, paid_at) ELSE null END as days_late

    from invoices

)

select * from payment_status
