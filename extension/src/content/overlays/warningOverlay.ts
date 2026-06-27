import type { PageAnalysis } from "../../shared/types/moderation";

const BANNER_ID = "webshield-warning-banner";

export function renderPageBanner(analysis: PageAnalysis): void {
  const existing = document.getElementById(BANNER_ID);
  existing?.remove();

  const banner = document.createElement("div");
  banner.id = BANNER_ID;
  banner.className = "webshield-warning-banner";
  banner.innerHTML = `
    <strong>WebShield:</strong>
    <span>Score ${analysis.summary.safety_score}/100 · ${analysis.summary.status}</span>
    <button type="button" data-action="toggle-panel">Details</button>
  `;

  banner.querySelector<HTMLButtonElement>("[data-action='toggle-panel']")?.addEventListener("click", () => {
    document.getElementById("webshield-explanation-panel")?.classList.toggle("is-open");
  });

  document.body.appendChild(banner);
}
