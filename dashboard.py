import duckdb
import streamlit as st
import plotly.express as px

DB_PATH = "data/github_analytics.duckdb"

st.set_page_config(page_title="GitHub Project Health Analytics", layout="wide")

st.title("GitHub Project Health Analytics Dashboard")
st.caption("Powered by GitHub API, DuckDB, dbt, Streamlit and Plotly")

@st.cache_data
def load_health_metrics():
    con = duckdb.connect(DB_PATH)
    df = con.execute("select * from github_project_health").df()
    con.close()
    return df

@st.cache_data
def load_commits():
    con = duckdb.connect(DB_PATH)
    df = con.execute("""
        select
            date_trunc('day', author_date) as commit_day,
            count(*) as commits
        from stg_commits
        group by 1
        order by 1
    """).df()
    con.close()
    return df

@st.cache_data
def load_issues():
    con = duckdb.connect(DB_PATH)
    df = con.execute("""
        select
            state,
            count(*) as issue_count
        from stg_issues
        group by 1
    """).df()
    con.close()
    return df

try:
    health = load_health_metrics()
    commits = load_commits()
    issues = load_issues()
except Exception:
    st.error("Run: python ingest_github.py, then dbt run --profiles-dir .")
    st.stop()

if health.empty:
    st.warning("No GitHub data found.")
    st.stop()

row = health.iloc[0]

st.subheader(row["full_name"])
st.write(row["description"])

col1, col2, col3, col4 = st.columns(4)

col1.metric("Stars", f"{row['stars']:,.0f}")
col2.metric("Forks", f"{row['forks']:,.0f}")
col3.metric("Open Issues", f"{row['open_issues']:,.0f}")
col4.metric("Contributors Sample", f"{row['contributors_sample']:,.0f}")

col5, col6, col7 = st.columns(3)

col5.metric("Issues Sample", f"{row['total_issues']:,.0f}")
col6.metric("PRs Sample", f"{row['total_prs']:,.0f}")
col7.metric("Commits Sample", f"{row['total_commits']:,.0f}")

st.subheader("Commit Activity")

fig_commits = px.line(
    commits,
    x="commit_day",
    y="commits",
    markers=True,
    title="Daily Commit Activity"
)
st.plotly_chart(fig_commits, use_container_width=True)

st.subheader("Issue Status")

fig_issues = px.bar(
    issues,
    x="state",
    y="issue_count",
    title="Open vs Closed Issues"
)
st.plotly_chart(fig_issues, use_container_width=True)

st.subheader("Repository Health Summary")

st.info(
    f"{row['full_name']} has {row['stars']:,.0f} stars and {row['forks']:,.0f} forks. "
    f"In the sampled API data, there are {row['total_issues']:,.0f} issues, "
    f"{row['total_prs']:,.0f} pull requests, and {row['total_commits']:,.0f} commits. "
    f"The average issue resolution time is {row['avg_issue_resolution_days']} days, "
    f"and the average PR merge time is {row['avg_pr_merge_days']} days. "
    f"This helps engineering and product teams monitor repository activity, project health, and delivery velocity."
)

st.subheader("Raw Health Metrics")
st.dataframe(health, use_container_width=True)