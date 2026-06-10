export type RepositoryInfo = {
  name: string;
  full_name: string;
  description?: string;
  html_url: string;
  stars: number;
  forks: number;
  open_issues: number;
  default_branch: string;
  language?: string;
  created_at: string;
  updated_at: string;
  license?: string;
};

export type FileChecks = {
  readme: boolean;
  license: boolean;
  gitignore: boolean;
  contributing: boolean;
  code_of_conduct: boolean;
  dockerfile: boolean;
  github_actions: boolean;
  env_example: boolean;
  tests_folder: boolean;
};

export type ScoreSection = {
  name: string;
  score: number;
  max_score: number;
  feedback: string;
};

export type AnalyzeResponse = {
  repository: RepositoryInfo;
  languages: Record<string, number>;
  files: FileChecks;
  score: number;
  sections: ScoreSection[];
  recommendations: string[];
};
