
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select region
from "saas_analytics"."main"."revenue_metrics"
where region is null



  
  
      
    ) dbt_internal_test