import os
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv
 
load_dotenv()
 
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
 
 
def _days_since(date_str: str) -> int:
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return (datetime.now(timezone.utc) - dt).days
    except Exception:
        return -1
 
 
def get_github_summary(repo_url: str) -> str:
    if not repo_url or "github.com" not in repo_url:
        return "No GitHub repository provided."
 
    try:
        parts = repo_url.rstrip("/").split("github.com/")[-1].split("/")
        if len(parts) < 2:
            return "Could not parse GitHub URL — provide a repo URL like https://github.com/org/repo"
        owner, repo = parts[0], parts[1]
    except Exception:
        return "Invalid GitHub URL format."
 
    headers = {}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    headers["Accept"] = "application/vnd.github.v3+json"
 
    base = f"https://api.github.com/repos/{owner}/{repo}"
 
    try:
        # Repo metadata
        meta_r = requests.get(base, headers=headers, timeout=10)
        if meta_r.status_code == 404:
            return "GitHub repository not found — may have been deleted after project collapse."
        meta_r.raise_for_status()
        meta = meta_r.json()
 
        stars = meta.get("stargazers_count", 0)
        forks = meta.get("forks_count", 0)
        open_issues = meta.get("open_issues_count", 0)
        archived = meta.get("archived", False)
        pushed_at = meta.get("pushed_at", "")
        days_since_push = _days_since(pushed_at) if pushed_at else -1
 
        # Recent commits
        commits_r = requests.get(
            f"{base}/commits?per_page=10",
            headers=headers,
            timeout=10,
        )
        commits_r.raise_for_status()
        commits = commits_r.json()
 
        if not isinstance(commits, list) or not commits:
            return (
                f"Repository exists but has no accessible commits. "
                f"Stars: {stars}. Archived: {archived}. "
                f"Last push: {pushed_at[:10] if pushed_at else 'unknown'}."
            )
 
        last_commit_date = commits[0]["commit"]["author"]["date"]
        last_commit_msg = commits[0]["commit"]["message"].split("\n")[0][:80]
        days_dead = _days_since(last_commit_date)
 
        activity_verdict = (
            "ACTIVE (commits within 30 days)" if days_dead < 30
            else f"ABANDONED — last commit {days_dead} days ago"
        )
 
        return (
            f"Repository: {owner}/{repo}. "
            f"Stars: {stars}. Forks: {forks}. Open issues: {open_issues}. "
            f"Archived by owner: {archived}. "
            f"Last commit: {last_commit_date[:10]} ({days_dead} days ago). "
            f"Last commit message: \"{last_commit_msg}\". "
            f"Recent commits retrieved: {len(commits)}. "
            f"Activity status: {activity_verdict}."
        )
 
    except requests.exceptions.Timeout:
        return "GitHub API timed out. Repository data unavailable."
    except requests.exceptions.RequestException as e:
        return f"GitHub data unavailable: {str(e)}"
