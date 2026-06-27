import type { PageAnalysis } from "../../shared/types/moderation";

const PANEL_ID = "webshield-explanation-panel";

export function renderExplanationPanel(analysis: PageAnalysis): void {
  const existing = document.getElementById(PANEL_ID);
  existing?.remove();

  const panel = document.createElement("aside");
  panel.id = PANEL_ID;
  panel.className = "webshield-explanation-panel";
  panel.innerHTML = `
    <div class="webshield-panel-header">
      <strong>WebShield analysis</strong>
      <button type="button" data-action="close">×</button>
    </div>
    <div class="webshield-panel-body">
      <p>${analysis.summary.explanation}</p>
      <p><strong>Safety score:</strong> ${analysis.summary.safety_score}/100</p>
      <p><strong>Preference match:</strong> ${analysis.summary.preference_match.score.toFixed(1)}%</p>
      <p><strong>Top interests:</strong> ${analysis.summary.preference_match.top_interests.join(", ") || "None"}</p>
      <ul>
        ${analysis.decisions
          .filter((decision) => decision.action !== "allow")
          .slice(0, 10)
          .map(
            (decision) =>
              `<li><strong>${decision.primary_category || "flagged"}</strong> — ${decision.action} — ${decision.explanation}</li>`
          )
          .join("")}
      </ul>
    </div>
  `;

  panel.querySelector<HTMLButtonElement>("[data-action='close']")?.addEventListener("click", () => {
    panel.classList.remove("is-open");
  });

  document.body.appendChild(panel);
}
