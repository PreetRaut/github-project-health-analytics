 select
    subscription_id,
    customer_id,
    plan,
    monthly_revenue,
    is_churned,
    created_at
from raw_subscriptions