import { useState } from 'react';
import { Github, Search } from 'lucide-react';
import { analyzeRepository } from './services/api';
import type { AnalyzeResponse } from './types';
import { ScoreCard } from './components/ScoreCard';
import { LanguageBar } from './components/LanguageBar';
import { Checklist } from './components/Checklist';
import './styles.css';

function App() {
  const [repoUrl, setRepoUrl] = useState('https://github.com/tiangolo/fastapi');
  const [result, setResult] = useState<AnalyzeResponse | null>(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const data = await analyzeRepository(repoUrl);
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unexpected error');
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="page">
      <section className="hero">
        <div className="badge"><Github size={18} /> GitHub Portfolio Tool</div>
        <h1>GitHub Repo Analyzer</h1>
        <p>Analyze repository quality, documentation, project hygiene and improvement opportunities in seconds.</p>

        <form onSubmit={handleSubmit} className="search-form">
          <input
            type="url"
            value={repoUrl}
            onChange={(event) => setRepoUrl(event.target.value)}
            placeholder="https://github.com/owner/repository"
            required
          />
          <button type="submit" disabled={loading}>
            <Search size={18} /> {loading ? 'Analyzing...' : 'Analyze'}
          </button>
        </form>
        {error && <p className="error">{error}</p>}
      </section>

      {result && (
        <section className="dashboard">
          <ScoreCard score={result.score} />

          <article className="card repo-card">
            <h2>{result.repository.full_name}</h2>
            <p>{result.repository.description ?? 'No description available.'}</p>
            <div className="stats">
              <span>★ {result.repository.stars}</span>
              <span>⑂ {result.repository.forks}</span>
              <span>Issues {result.repository.open_issues}</span>
              <span>Branch {result.repository.default_branch}</span>
            </div>
            <a href={result.repository.html_url} target="_blank" rel="noreferrer">Open repository</a>
          </article>

          <article className="card">
            <h2>Quality Sections</h2>
            <div className="section-list">
              {result.sections.map((section) => (
                <div key={section.name} className="section-item">
                  <div>
                    <strong>{section.name}</strong>
                    <p>{section.feedback}</p>
                  </div>
                  <span>{section.score}/{section.max_score}</span>
                </div>
              ))}
            </div>
          </article>

          <article className="card">
            <h2>Languages</h2>
            <LanguageBar languages={result.languages} />
          </article>

          <article className="card">
            <h2>Project Checklist</h2>
            <Checklist files={result.files} />
          </article>

          <article className="card recommendations">
            <h2>Recommendations</h2>
            <ul>
              {result.recommendations.map((item) => <li key={item}>{item}</li>)}
            </ul>
          </article>
        </section>
      )}
    </main>
  );
}

export default App;
