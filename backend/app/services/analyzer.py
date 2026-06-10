from typing import Dict, List

from app.models import AnalyzeResponse, FileChecks, RepositoryInfo, ScoreSection
from app.services.github_client import GitHubClient


class RepositoryAnalyzer:
    def __init__(self, github_client: GitHubClient) -> None:
        self.github = github_client

    async def analyze(self, repo_url: str) -> AnalyzeResponse:
        owner, repo = self.github.parse_repo_url(repo_url)
        repository = await self.github.get_repository(owner, repo)
        languages = await self.github.get_languages(owner, repo)
        root_contents = await self.github.get_root_contents(owner, repo)
        workflows = await self.github.get_directory_contents(owner, repo, ".github/workflows")

        root_names = {item["name"].lower() for item in root_contents}
        root_dirs = {item["name"].lower() for item in root_contents if item.get("type") == "dir"}

        checks = FileChecks(
            readme=any(name.startswith("readme") for name in root_names),
            license=any(name.startswith("license") for name in root_names),
            gitignore=".gitignore" in root_names,
            contributing=any(name.startswith("contributing") for name in root_names),
            code_of_conduct=any("code_of_conduct" in name or "code-of-conduct" in name for name in root_names),
            dockerfile="dockerfile" in root_names,
            github_actions=bool(workflows),
            env_example=".env.example" in root_names or "env.example" in root_names,
            tests_folder="tests" in root_dirs or "test" in root_dirs,
        )

        sections = self._build_sections(repository, languages, checks)
        total_score = round(sum(section.score for section in sections) / sum(section.max_score for section in sections) * 100)
        recommendations = self._build_recommendations(checks, repository, languages)

        return AnalyzeResponse(
            repository=RepositoryInfo(
                name=repository["name"],
                full_name=repository["full_name"],
                description=repository.get("description"),
                html_url=repository["html_url"],
                stars=repository["stargazers_count"],
                forks=repository["forks_count"],
                open_issues=repository["open_issues_count"],
                default_branch=repository["default_branch"],
                language=repository.get("language"),
                created_at=repository["created_at"],
                updated_at=repository["updated_at"],
                license=repository["license"]["name"] if repository.get("license") else None,
            ),
            languages=languages,
            files=checks,
            score=total_score,
            sections=sections,
            recommendations=recommendations,
        )

    def _build_sections(self, repo: Dict, languages: Dict[str, int], checks: FileChecks) -> List[ScoreSection]:
        documentation_score = sum([checks.readme, checks.license, checks.contributing, checks.code_of_conduct]) * 5
        maintainability_score = sum([checks.gitignore, checks.tests_folder, checks.github_actions, checks.dockerfile, checks.env_example]) * 4
        activity_score = 20 if repo.get("pushed_at") else 8
        popularity_score = min(20, repo.get("stargazers_count", 0) // 10 + repo.get("forks_count", 0) // 5)
        stack_score = 20 if len(languages) >= 2 else 12 if len(languages) == 1 else 5

        return [
            ScoreSection(name="Documentation", score=documentation_score, max_score=20, feedback="README, license and community files."),
            ScoreSection(name="Maintainability", score=maintainability_score, max_score=20, feedback="Project hygiene, tests, CI and environment files."),
            ScoreSection(name="Activity", score=activity_score, max_score=20, feedback="Recent repository activity indicators."),
            ScoreSection(name="Popularity", score=popularity_score, max_score=20, feedback="Stars and forks as public interest signals."),
            ScoreSection(name="Tech Stack", score=stack_score, max_score=20, feedback="Language diversity and detectable stack."),
        ]

    def _build_recommendations(self, checks: FileChecks, repo: Dict, languages: Dict[str, int]) -> List[str]:
        recommendations: List[str] = []
        if not checks.readme:
            recommendations.append("Add a professional README with setup, usage, screenshots and roadmap.")
        if not checks.license:
            recommendations.append("Add a LICENSE file to clarify how others can use the project.")
        if not checks.tests_folder:
            recommendations.append("Create a tests folder and add automated tests for the core logic.")
        if not checks.github_actions:
            recommendations.append("Add GitHub Actions to run tests automatically on every push.")
        if not checks.env_example:
            recommendations.append("Add a .env.example file to document required environment variables.")
        if not checks.dockerfile:
            recommendations.append("Consider adding Docker support for easier local and cloud deployment.")
        if not languages:
            recommendations.append("GitHub could not detect languages. Check if source files are present.")
        if repo.get("open_issues_count", 0) > 20:
            recommendations.append("Review open issues and close stale or duplicated items.")
        if not recommendations:
            recommendations.append("The repository has strong baseline quality. Consider adding demos, badges and architecture docs.")
        return recommendations
