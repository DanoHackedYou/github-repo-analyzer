<<<<<<< HEAD
# GitHub Repo Analyzer

A professional full-stack dashboard that analyzes public GitHub repositories and generates a quality score, project hygiene checklist, language breakdown and improvement recommendations.

## Screenshot

Add a screenshot here after running the project locally:

```md
![GitHub Repo Analyzer screenshot](docs/screenshot.png)
```

## Features

- Analyze any public GitHub repository URL.
- Fetch repository metadata using the GitHub REST API.
- Detect important project files such as README, LICENSE, Dockerfile and GitHub Actions workflows.
- Calculate a repository quality score from documentation, maintainability, activity, popularity and stack signals.
- Display language usage percentages.
- Generate practical recommendations to improve the repository.
- Full-stack architecture with FastAPI and React.
- Docker support and GitHub Actions CI.

## Technologies

### Backend

- Python 3.12
- FastAPI
- Pydantic
- HTTPX
- Uvicorn

### Frontend

- React
- TypeScript
- Vite
- CSS
- Lucide React

### DevOps

- Docker
- Docker Compose
- GitHub Actions

## Project Structure

```txt
github-repo-analyzer/
├── .github/workflows/ci.yml
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   └── services/
│   │       ├── analyzer.py
│   │       └── github_client.py
│   ├── .env.example
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Checklist.tsx
│   │   │   ├── LanguageBar.tsx
│   │   │   └── ScoreCard.tsx
│   │   ├── services/api.ts
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   ├── styles.css
│   │   └── types.ts
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── .gitignore
├── docker-compose.yml
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone URL_DEL_REPOSITORIO
cd github-repo-analyzer
```

### 2. Configure backend environment

```bash
cd backend
copy .env.example .env
```

On macOS/Linux:

```bash
cp .env.example .env
```

`GITHUB_TOKEN` is optional for public repositories, but recommended to avoid rate limits.

### 3. Run the backend

Windows PowerShell:

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

macOS/Linux:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API will be available at:

```txt
http://localhost:8000
```

Interactive API docs:

```txt
http://localhost:8000/docs
```

### 4. Run the frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at:

```txt
http://localhost:5173
```

## Docker Usage

Create `backend/.env` first, then run:

```bash
docker compose up --build
```

## Environment Variables

| Variable | Required | Description |
| --- | --- | --- |
| `GITHUB_TOKEN` | No | GitHub personal access token used to increase API rate limits. |

## Example Usage

Paste a public repository URL:

```txt
https://github.com/tiangolo/fastapi
```

The app returns:

- Repository metadata.
- Quality score.
- File checklist.
- Language usage.
- Improvement recommendations.

## Roadmap

- Add authentication and saved analyses.
- Add PDF export.
- Add AI-generated README improvement suggestions.
- Add historical score tracking.
- Add comparison between two repositories.
- Add test coverage metrics.
- Add deployment templates for Render and Vercel.

## Contributing

Contributions are welcome. Open an issue first to discuss major changes.

## License

MIT License. Add a `LICENSE` file before publishing if you want the project to be reusable.

## Author

Created as a professional portfolio project.

## Status

MVP ready for local execution and GitHub publication.
=======
# github-repo-analyzer
Full-stack dashboard to analyze GitHub repository quality, documentation and project hygiene.
>>>>>>> d2238071fde1e431ab4a648a75f113a4c5b0411a
