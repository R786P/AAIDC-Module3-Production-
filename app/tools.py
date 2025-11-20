from crewai_tools import Tool
import requests
from urllib.parse import urlparse

class ReadGitHubReadmeTool(BaseTool):
    name: str = "Read GitHub README"
    description: str = "Fetches the README.md content from a GitHub repository."

    def _run(self, repo_url: str) -> str:
        try:
            # Parse URL
            path = urlparse(repo_url).path
            owner, repo = path.strip("/").split("/")[:2]

            # GitHub API se README fetch karein
            api_url = f"https://api.github.com/repos/{owner}/{repo}/readme"
            headers = {"Accept": "application/vnd.github.v3.raw"}
            response = requests.get(api_url, headers=headers)

            if response.status_code == 200:
                return response.text[:2000]  # First 2000 chars
            else:
                return "README not found"
        except Exception as e:
            return f"Error reading repo: {str(e)}"
