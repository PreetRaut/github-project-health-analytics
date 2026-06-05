
  
  create view "saas_analytics"."main"."stg_subscriptions__dbt_tmp" as (
    select
    subscription_id,
    customer_id,
    plan,
    monthly_revenue,
    is_churned,
    created_at
from raw_subscriptions
  );
