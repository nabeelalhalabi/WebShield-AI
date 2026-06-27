import { truncateText } from "../../shared/utils/text";
import type { ContentDecision } from "../../shared/types/moderation";

interface Props {
  decisions: ContentDecision[];
}

export function RecentDecisions({ decisions }: Props) {
  const visible = decisions.filter((decision) => decision.action !== "allow").slice(0, 5);

  return (
    <section className="card">
      <h2>Recent decisions</h2>
      {visible.length === 0 ? (
        <p className="muted">Nothing flagged on the current page.</p>
      ) : (
        <ul className="plain-list">
          {visible.map((decision) => (
            <li key={decision.item_id}>
              <div>
                <strong>{decision.primary_category || "flagged"}</strong>
                <div className="muted">{decision.action}</div>
              </div>
              <span>{truncateText(decision.explanation, 70)}</span>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
