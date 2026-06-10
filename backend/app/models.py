from pydantic import BaseModel, Field, HttpUrl
from typing import Dict, List, Optional


class AnalyzeRequest(BaseModel):
    repo_url: str = Field(..., examples=["https://github.com/tiangolo/fastapi"])


class RepositoryInfo(BaseModel):
    name: str
    full_name: str
    description: Optional[str] = None
    html_url: HttpUrl
    stars: int
    forks: int
    open_issues: int
    default_branch: str
    language: Optional[str] = None
    created_at: str
    updated_at: str
    license: Optional[str] = None


class FileChecks(BaseModel):
    readme: bool
    license: bool
    gitignore: bool
    contributing: bool
    code_of_conduct: bool
    dockerfile: bool
    github_actions: bool
    env_example: bool
    tests_folder: bool


class ScoreSection(BaseModel):
    name: str
    score: int
    max_score: int
    feedback: str


class AnalyzeResponse(BaseModel):
    repository: RepositoryInfo
    languages: Dict[str, int]
    files: FileChecks
    score: int
    sections: List[ScoreSection]
    recommendations: List[str]
