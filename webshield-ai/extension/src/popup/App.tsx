import { useEffect, useState } from "react";

import { PageSummary } from "./components/PageSummary";
import { RecentDecisions } from "./components/RecentDecisions";
import { SafetyScoreCard } from "./components/SafetyScoreCard";
import { ToggleList } from "./components/ToggleList";
import {
  loadPopupState,
  openHistoryPage,
  openOptionsPage,
  rescanCurrentTab,
  restoreCurrentTab,
  toggleEnabled
} from "./store/popupStore";
import type { PageAnalysis } from "../shared/types/moderation";
import type { UserSettings } from "../shared/types/settings";

export default function App() {
  const [analysis, setAnalysis] = useState<PageAnalysis | null>(null);
  const [settings, setSettings] = useState<UserSettings | null>(null);
  const [loading, setLoading] = useState(true);

  async function refresh(): Promise<void> {
    setLoading(true);
    const state = await loadPopupState();
    setAnalysis(state.analysis);
    setSettings(state.settings);
    setLoading(false);
  }

  useEffect(() => {
    refresh().catch(console.error);
  }, []);

  if (loading || !settings) {
    return <main className="page-shell"><p>Loading…</p></main>;
  }

  return (
    <main className="page-shell">
      <header className="page-header">
        <h1>WebShield AI</h1>
        <button className="secondary" onClick={() => toggleEnabled(settings).then(setSettings)}>
          {settings.enabled ? "Disable" : "Enable"}
        </button>
      </header>

      <SafetyScoreCard summary={analysis?.summary ?? null} />
      <PageSummary analysis={analysis} />
      <ToggleList detectors={settings.detectors} />
      <RecentDecisions decisions={analysis?.decisions ?? []} />

      <section className="card actions-row">
        <button onClick={() => rescanCurrentTab().then(refresh)}>Rescan</button>
        <button className="secondary" onClick={() => restoreCurrentTab().then(refresh)}>Restore</button>
      </section>

      <section className="card actions-row">
        <button className="secondary" onClick={() => openOptionsPage()}>Options</button>
        <button className="secondary" onClick={() => openHistoryPage()}>History</button>
      </section>
    </main>
  );
}
