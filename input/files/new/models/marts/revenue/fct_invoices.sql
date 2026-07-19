{{ config(materialized='table') }}

with invoices as (

    select * from {{ ref('int_invoice_payments') }}

),

accounts as (

    select * from {{ ref('dim_accounts') }}

),

final as (

    select
        i.invoice_id,
        i.account_id,
        a.account_name,
        i.amount_due,
        i.invoice_date,
        i.due_date,
        i.paid_at,
        i.status,
        i.days_late,
        IFF(i.paid_at is not null, 'paid', 'outstanding')  as payment_status_label
    from invoices i
    inner join accounts a
        on i.account_id = a.account_id

)

select * from final
