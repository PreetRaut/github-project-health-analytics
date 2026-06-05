select
    issue_id,
    issue_number,
    title,
    state,
    cast(created_at as timestamp) as created_at,
    cast(closed_at as timestamp) as closed_at,
    user_login,
    comments
from raw_issues