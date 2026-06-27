import type { DetectorToggles } from "../../shared/types/settings";

interface Props {
  detectors: DetectorToggles;
}

export function ToggleList({ detectors }: Props) {
  return (
    <section className="card">
      <h2>Enabled detectors</h2>
      <ul className="plain-list">
        {Object.entries(detectors).map(([key, value]) => (
          <li key={key}>
            <span>{key.replaceAll("_", " ")}</span>
            <strong>{value ? "On" : "Off"}</strong>
          </li>
        ))}
      </ul>
    </section>
  );
}
