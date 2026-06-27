import { ACTION_LABELS, CATEGORY_LABELS } from "../../shared/constants/actions";
import type { ActionType, UserSettings } from "../../shared/types/settings";

interface Props {
  settings: UserSettings;
  onThresholdChange: (category: string, value: number) => void;
  onActionChange: (category: string, value: ActionType) => void;
}

export function ActionSettings({ settings, onThresholdChange, onActionChange }: Props) {
  return (
    <section className="card">
      <h2>Actions and thresholds</h2>
      <div className="settings-grid">
        {Object.keys(settings.thresholds).map((category) => (
          <div className="grid-row" key={category}>
            <div>
              <strong>{CATEGORY_LABELS[category] || category}</strong>
              <div className="muted">Threshold: {settings.thresholds[category].toFixed(2)}</div>
            </div>
            <input
              type="range"
              min={0}
              max={1}
              step={0.05}
              value={settings.thresholds[category]}
              onChange={(event) => onThresholdChange(category, Number(event.target.value))}
            />
            <select
              value={settings.category_actions[category]}
              onChange={(event) => onActionChange(category, event.target.value as ActionType)}
            >
              {Object.entries(ACTION_LABELS).map(([value, label]) => (
                <option value={value} key={value}>
                  {label}
                </option>
              ))}
            </select>
          </div>
        ))}
      </div>
    </section>
  );
}
