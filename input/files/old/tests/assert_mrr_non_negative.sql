{{ config(severity='error') }}

select *
from {{ ref('fct_mrr_monthly') }}
where mrr_amount < 0
