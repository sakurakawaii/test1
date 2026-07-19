{{ config(materialized='table') }}

with plans as (

    select * from {{ ref('plan_tiers') }}

)

select * from plans
