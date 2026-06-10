import os
import re
from typing import Any, Dict, List, Optional

import httpx


class GitHubClientError(Exception):
    pass


class GitHubClient:
    def __init__(self) -> None:
        self.base_url = "https://api.github.com"
        self.token = os.getenv("GITHUB_TOKEN")
        self.headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"

    @staticmethod
    def parse_repo_url(repo_url: str) -> tuple[str, str]:
        pattern = r"github\.com[:/](?P<owner>[A-Za-z0-9_.-]+)/(?P<repo>[A-Za-z0-9_.-]+)"
        match = re.search(pattern, repo_url.strip().replace(".git", ""))
        if not match:
            raise GitHubClientError("Invalid GitHub repository URL.")
        return match.group("owner"), match.group("repo")

    async def _get(self, endpoint: str) -> Any:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(f"{self.base_url}{endpoint}", headers=self.headers)

        if response.status_code == 404:
            raise GitHubClientError("Repository or resource not found.")
        if response.status_code == 403:
            raise GitHubClientError("GitHub API rate limit reached or access forbidden. Add a GITHUB_TOKEN.")
        if response.status_code >= 400:
            raise GitHubClientError(f"GitHub API error: {response.status_code}")
        return response.json()

    async def get_repository(self, owner: str, repo: str) -> Dict[str, Any]:
        return await self._get(f"/repos/{owner}/{repo}")

    async def get_languages(self, owner: str, repo: str) -> Dict[str, int]:
        return await self._get(f"/repos/{owner}/{repo}/languages")

    async def get_root_contents(self, owner: str, repo: str) -> List[Dict[str, Any]]:
        return await self._get(f"/repos/{owner}/{repo}/contents")

    async def get_directory_contents(self, owner: str, repo: str, path: str) -> Optional[List[Dict[str, Any]]]:
        try:
            data = await self._get(f"/repos/{owner}/{repo}/contents/{path}")
            return data if isinstance(data, list) else None
        except GitHubClientError:
            return None
