with repo as (
    select *
    from {{ ref('stg_repo') }}
),

issues as (
    select *
    from {{ ref('stg_issues') }}
),

prs as (
    select *
    from {{ ref('stg_pull_requests') }}
),

commits as (
    select *
    from {{ ref('stg_commits') }}
),

issue_metrics as (
    select
        count(*) as total_issues,
        count(case when state = 'open' then 1 end) as open_issues_sample,
        count(case when state = 'closed' then 1 end) as closed_issues_sample,
        avg(date_diff('day', created_at, closed_at)) as avg_issue_resolution_days
    from issues
    where closed_at is not null
),

pr_metrics as (
    select
        count(*) as total_prs,
        count(case when merged_at is not null then 1 end) as merged_prs,
        avg(date_diff('day', created_at, merged_at)) as avg_pr_merge_days
    from prs
),

commit_metrics as (
    select
        count(*) as total_commits,
        count(distinct author_name) as contributors_sample,
        min(author_date) as first_commit_sample,
        max(author_date) as latest_commit_sample
    from commits
)

select
    r.full_name,
    r.description,
    r.language,
    r.stars,
    r.forks,
    r.open_issues,
    i.total_issues,
    i.open_issues_sample,
    i.closed_issues_sample,
    round(i.avg_issue_resolution_days, 2) as avg_issue_resolution_days,
    p.total_prs,
    p.merged_prs,
    round(p.avg_pr_merge_days, 2) as avg_pr_merge_days,
    c.total_commits,
    c.contributors_sample,
    c.first_commit_sample,
    c.latest_commit_sample
from repo r
cross join issue_metrics i
cross join pr_metrics p
cross join commit_metrics c