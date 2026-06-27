import type { DetectorToggles } from "../../shared/types/settings";

interface Props {
  detectors: DetectorToggles;
  scan_on_load: boolean;
  onToggle: (key: keyof DetectorToggles, value: boolean) => void;
  onScanOnLoadChange: (value: boolean) => void;
}

export function DetectionSettings({ detectors, scan_on_load, onToggle, onScanOnLoadChange }: Props) {
  return (
    <section className="card">
      <h2>Detection settings</h2>
      <label className="checkbox-row">
        <input
          type="checkbox"
          checked={scan_on_load}
          onChange={(event) => onScanOnLoadChange(event.target.checked)}
        />
        <span>Scan automatically on page load</span>
      </label>

      <div className="settings-grid">
        {Object.entries(detectors).map(([key, value]) => (
          <label className="checkbox-row" key={key}>
            <input
              type="checkbox"
              checked={value}
              onChange={(event) => onToggle(key as keyof DetectorToggles, event.target.checked)}
            />
            <span>{key.replaceAll("_", " ")}</span>
          </label>
        ))}
      </div>
    </section>
  );
}
