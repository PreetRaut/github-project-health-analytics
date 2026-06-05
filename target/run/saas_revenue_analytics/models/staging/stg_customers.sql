
  
  create view "saas_analytics"."main"."stg_customers__dbt_tmp" as (
    select
    customer_id,
    region,
    segment,
    signup_date
from raw_customers
  );
