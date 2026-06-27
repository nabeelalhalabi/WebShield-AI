import type { PageAnalysis } from "../../shared/types/moderation";

interface Props {
  analysis: PageAnalysis | null;
}

export function PageSummary({ analysis }: Props) {
  return (
    <section className="card">
      <h2>Page summary</h2>
      {analysis ? (
        <>
          <p><strong>{analysis.summary.title}</strong></p>
          <p className="muted">{analysis.summary.url}</p>
          <p>{analysis.summary.explanation}</p>
        </>
      ) : (
        <p className="muted">Open a regular web page and scan it to see results here.</p>
      )}
    </section>
  );
}
