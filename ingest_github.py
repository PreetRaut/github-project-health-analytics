import os
import requests
import duckdb
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("GITHUB_REPO", "microsoft/playwright")
DB_PATH = "data/github_analytics.duckdb"

HEADERS = {
    "Accept": "application/vnd.github+json"
}

if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"


def fetch_paginated(endpoint, max_pages=3):
    rows = []

    for page in range(1, max_pages + 1):
        url = f"https://api.github.com/repos/{REPO}/{endpoint}"
        params = {"per_page": 100, "page": page}

        response = requests.get(url, headers=HEADERS, params=params)

        if response.status_code != 200:
            raise Exception(f"GitHub API error: {response.status_code} - {response.text}")

        data = response.json()

        if not data:
            break

        rows.extend(data)

    return rows


def fetch_repo():
    url = f"https://api.github.com/repos/{REPO}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        raise Exception(f"GitHub API error: {response.status_code} - {response.text}")

    repo = response.json()

    return pd.DataFrame([{
        "repo_id": repo.get("id"),
        "repo_name": repo.get("name"),
        "full_name": repo.get("full_name"),
        "description": repo.get("description"),
        "stars": repo.get("stargazers_count"),
        "forks": repo.get("forks_count"),
        "open_issues": repo.get("open_issues_count"),
        "language": repo.get("language"),
        "created_at": repo.get("created_at"),
        "updated_at": repo.get("updated_at")
    }])


def fetch_issues():
    issues = fetch_paginated("issues?state=all", max_pages=3)
    rows = []

    for issue in issues:
        if "pull_request" in issue:
            continue

        rows.append({
            "issue_id": issue.get("id"),
            "issue_number": issue.get("number"),
            "title": issue.get("title"),
            "state": issue.get("state"),
            "created_at": issue.get("created_at"),
            "closed_at": issue.get("closed_at"),
            "user_login": issue.get("user", {}).get("login"),
            "comments": issue.get("comments")
        })

    return pd.DataFrame(rows)


def fetch_pull_requests():
    prs = fetch_paginated("pulls?state=all", max_pages=3)
    rows = []

    for pr in prs:
        rows.append({
            "pr_id": pr.get("id"),
            "pr_number": pr.get("number"),
            "title": pr.get("title"),
            "state": pr.get("state"),
            "created_at": pr.get("created_at"),
            "closed_at": pr.get("closed_at"),
            "merged_at": pr.get("merged_at"),
            "user_login": pr.get("user", {}).get("login")
        })

    return pd.DataFrame(rows)


def fetch_commits():
    commits = fetch_paginated("commits", max_pages=3)
    rows = []

    for commit in commits:
        rows.append({
            "sha": commit.get("sha"),
            "author_name": commit.get("commit", {}).get("author", {}).get("name"),
            "author_date": commit.get("commit", {}).get("author", {}).get("date"),
            "message": commit.get("commit", {}).get("message")
        })

    return pd.DataFrame(rows)


def save_to_duckdb(repo_df, issues_df, prs_df, commits_df):
    os.makedirs("data", exist_ok=True)

    con = duckdb.connect(DB_PATH)

    con.register("repo_df", repo_df)
    con.register("issues_df", issues_df)
    con.register("prs_df", prs_df)
    con.register("commits_df", commits_df)

    con.execute("CREATE OR REPLACE TABLE raw_repo AS SELECT * FROM repo_df")
    con.execute("CREATE OR REPLACE TABLE raw_issues AS SELECT * FROM issues_df")
    con.execute("CREATE OR REPLACE TABLE raw_pull_requests AS SELECT * FROM prs_df")
    con.execute("CREATE OR REPLACE TABLE raw_commits AS SELECT * FROM commits_df")

    con.close()


def main():
    print(f"Fetching GitHub repository data for {REPO}...")

    repo_df = fetch_repo()
    issues_df = fetch_issues()
    prs_df = fetch_pull_requests()
    commits_df = fetch_commits()

    save_to_duckdb(repo_df, issues_df, prs_df, commits_df)

    print("GitHub data loaded successfully.")
    print(f"Repository: {len(repo_df)}")
    print(f"Issues: {len(issues_df)}")
    print(f"Pull requests: {len(prs_df)}")
    print(f"Commits: {len(commits_df)}")


if __name__ == "__main__":
    main()