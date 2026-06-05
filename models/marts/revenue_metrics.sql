select
    c.region,
    c.segment,
    count(distinct c.customer_id) as total_customers,
    sum(s.monthly_revenue) as total_mrr,
    sum(s.monthly_revenue) * 12 as total_arr,
    sum(case when s.is_churned = 1 then 1 else 0 end) as churned_customers,
    round(
        sum(case when s.is_churned = 1 then 1 else 0 end) * 100.0
        / count(distinct c.customer_id),
        2
    ) as churn_rate_percent,
    avg(s.monthly_revenue) as average_revenue_per_customer
from {{ ref('stg_customers') }} c
join {{ ref('stg_subscriptions') }} s
    on c.customer_id = s.customer_id
group by
    c.region,
    c.segment