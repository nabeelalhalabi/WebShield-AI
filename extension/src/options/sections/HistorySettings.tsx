interface Props {
  history_enabled: boolean;
  enabled: boolean;
  onHistoryChange: (value: boolean) => void;
  onEnabledChange: (value: boolean) => void;
}

export function HistorySettings({
  history_enabled,
  enabled,
  onHistoryChange,
  onEnabledChange
}: Props) {
  return (
    <section className="card">
      <h2>General settings</h2>
      <label className="checkbox-row">
        <input type="checkbox" checked={enabled} onChange={(event) => onEnabledChange(event.target.checked)} />
        <span>Enable WebShield</span>
      </label>
      <label className="checkbox-row">
        <input
          type="checkbox"
          checked={history_enabled}
          onChange={(event) => onHistoryChange(event.target.checked)}
        />
        <span>Save page history on the backend</span>
      </label>
    </section>
  );
}
