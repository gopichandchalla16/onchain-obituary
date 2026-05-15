import requests
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")


def get_github_summary(repo_url):
    if not repo_url or "github.com" not in repo_url:
        return "No GitHub repository provided."
    try:
        parts = repo_url.rstrip("/").split("github.com/")[-1].split("/")
        owner, repo = parts[0], parts[1]
        headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}
        r = requests.get(
            f"https://api.github.com/repos/{owner}/{repo}/commits?per_page=10",
            headers=headers,
            timeout=10,
        )
        commits = r.json()
        if isinstance(commits, list) and commits:
            last_commit = commits[0]["commit"]["author"]["date"]
            return f"Last commit: {last_commit}. Recent commits retrieved: {len(commits)}."
        return "Repository abandoned — no commits accessible or repo deleted."
    except Exception as e:
        return f"GitHub data unavailable: {str(e)}"
