{{ config(materialized='table') }}

with adoption as (

    select * from {{ ref('int_feature_adoption') }}

),

accounts as (

    select * from {{ ref('dim_accounts') }}

),

legacy_flags as (

    select distinct flag_name
    from adoption
    where flag_name ilike '%legacy%'

),

final as (

    select
        a.account_id,
        a.account_name,
        COUNT(DISTINCT ad.flag_name)          as features_adopted_count

    from accounts a
    left join adoption ad
        on a.account_id = ad.account_id
    group by a.account_id, a.account_name

)

select * from final
