type LanguageBarProps = {
  languages: Record<string, number>;
};

export function LanguageBar({ languages }: LanguageBarProps) {
  const total = Object.values(languages).reduce((sum, value) => sum + value, 0);
  const entries = Object.entries(languages).sort((a, b) => b[1] - a[1]);

  if (!entries.length) {
    return <p className="muted">No languages detected.</p>;
  }

  return (
    <div className="language-list">
      {entries.map(([language, bytes]) => {
        const percent = total > 0 ? Math.round((bytes / total) * 100) : 0;
        return (
          <div key={language} className="language-item">
            <div className="language-row">
              <span>{language}</span>
              <span>{percent}%</span>
            </div>
            <div className="progress">
              <div style={{ width: `${percent}%` }} />
            </div>
          </div>
        );
      })}
    </div>
  );
}
