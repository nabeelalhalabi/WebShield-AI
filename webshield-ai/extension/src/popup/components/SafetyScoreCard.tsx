import type { PageSummary } from "../../shared/types/moderation";

interface Props {
  summary: PageSummary | null;
}

export function SafetyScoreCard({ summary }: Props) {
  const score = summary?.safety_score ?? 0;
  const status = summary?.status ?? "unknown";

  return (
    <section className="card">
      <h2>Safety</h2>
      <div className="score">{score}</div>
      <p className={`status status-${status}`}>{status}</p>
      <small>{summary ? `${summary.flagged_items} flagged item(s)` : "No page scanned yet"}</small>
    </section>
  );
}
