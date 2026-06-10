from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.models import AnalyzeRequest, AnalyzeResponse
from app.services.analyzer import RepositoryAnalyzer
from app.services.github_client import GitHubClient, GitHubClientError

app = FastAPI(
    title="GitHub Repo Analyzer API",
    description="Analyze GitHub repositories and generate quality recommendations.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze_repository(payload: AnalyzeRequest) -> AnalyzeResponse:
    try:
        analyzer = RepositoryAnalyzer(GitHubClient())
        return await analyzer.analyze(payload.repo_url)
    except GitHubClientError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
