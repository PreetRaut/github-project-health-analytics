select
    pr_id,
    pr_number,
    title,
    state,
    cast(created_at as timestamp) as created_at,
    cast(closed_at as timestamp) as closed_at,
    cast(merged_at as timestamp) as merged_at,
    user_login
from raw_pull_requests