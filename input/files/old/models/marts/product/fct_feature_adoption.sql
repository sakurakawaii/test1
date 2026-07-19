{{ config(materialized='table') }}

with adoption as (

    select * from {{ ref('int_feature_adoption') }}

),

accounts as (

    select * from {{ ref('dim_accounts') }}

),

final as (

    select
        a.account_id,
        a.account_name,
        (
            select COUNT(DISTINCT ad.flag_name)
            from adoption ad
            where ad.account_id = a.account_id
        )                                          as features_adopted_count

    from accounts a

)

select * from final
