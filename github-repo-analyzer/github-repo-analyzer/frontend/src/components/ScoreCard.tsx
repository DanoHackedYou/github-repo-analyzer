type ScoreCardProps = {
  score: number;
};

export function ScoreCard({ score }: ScoreCardProps) {
  const label = score >= 80 ? 'Excellent' : score >= 60 ? 'Good' : score >= 40 ? 'Needs work' : 'Poor';

  return (
    <section className="score-card">
      <p>Repository Quality Score</p>
      <strong>{score}/100</strong>
      <span>{label}</span>
    </section>
  );
}
