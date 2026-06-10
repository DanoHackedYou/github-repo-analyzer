import type { FileChecks } from '../types';

const labels: Record<keyof FileChecks, string> = {
  readme: 'README.md',
  license: 'LICENSE',
  gitignore: '.gitignore',
  contributing: 'CONTRIBUTING.md',
  code_of_conduct: 'Code of Conduct',
  dockerfile: 'Dockerfile',
  github_actions: 'GitHub Actions',
  env_example: '.env.example',
  tests_folder: 'Tests folder',
};

type ChecklistProps = {
  files: FileChecks;
};

export function Checklist({ files }: ChecklistProps) {
  return (
    <div className="checklist">
      {Object.entries(files).map(([key, value]) => (
        <div key={key} className="check-item">
          <span className={value ? 'ok' : 'missing'}>{value ? '✓' : '×'}</span>
          <span>{labels[key as keyof FileChecks]}</span>
        </div>
      ))}
    </div>
  );
}
