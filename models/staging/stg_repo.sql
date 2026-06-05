select
    repo_id,
    repo_name,
    full_name,
    description,
    stars,
    forks,
    open_issues,
    language,
    cast(created_at as timestamp) as created_at,
    cast(updated_at as timestamp) as updated_at
from raw_repo