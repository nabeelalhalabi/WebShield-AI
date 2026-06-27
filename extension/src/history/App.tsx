import { useEffect, useState } from "react";

import { clearHistory, listHistory } from "../shared/api/historyApi";

interface HistoryItem {
  id: number;
  title: string;
  url: string;
  status: string;
  safety_score: number;
  created_at: string;
}

export default function App() {
  const [items, setItems] = useState<HistoryItem[]>([]);
  const [status, setStatus] = useState("Loading…");

  async function refresh(): Promise<void> {
    try {
      const response = await listHistory();
      setItems(response.items as HistoryItem[]);
      setStatus("");
    } catch (error) {
      setStatus(error instanceof Error ? error.message : "Failed to load history.");
    }
  }

  useEffect(() => {
    refresh().catch(console.error);
  }, []);

  return (
    <main className="page-shell wide">
      <header className="page-header">
        <div>
          <h1>Scan history</h1>
          <p className="muted">Recent page summaries stored by the backend.</p>
        </div>
        <button
          className="secondary"
          onClick={() =>
            clearHistory().then(() => {
              setItems([]);
              setStatus("History cleared.");
            })
          }
        >
          Clear history
        </button>
      </header>

      {status ? <p className="muted">{status}</p> : null}

      <section className="card">
        {items.length === 0 ? (
          <p className="muted">No history records available.</p>
        ) : (
          <ul className="plain-list">
            {items.map((item) => (
              <li key={item.id}>
                <div>
                  <strong>{item.title}</strong>
                  <div className="muted">{item.url}</div>
                </div>
                <div>
                  <strong>{item.safety_score}</strong>
                  <div className="muted">{item.status}</div>
                </div>
              </li>
            ))}
          </ul>
        )}
      </section>
    </main>
  );
}
