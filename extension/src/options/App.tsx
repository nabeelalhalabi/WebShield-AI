import { useEffect, useState } from "react";

import type { ActionType, UserSettings } from "../shared/types/settings";
import { DetectionSettings } from "./sections/DetectionSettings";
import { ActionSettings } from "./sections/ActionSettings";
import { ChildSafeMode } from "./sections/ChildSafeMode";
import { DomainRules } from "./sections/DomainRules";
import { HistorySettings } from "./sections/HistorySettings";
import { PreferenceSettings } from "./sections/PreferenceSettings";
import { loadOptions, resetOptions, saveOptions } from "./store/optionsStore";

export default function App() {
  const [settings, setSettings] = useState<UserSettings | null>(null);
  const [status, setStatus] = useState("Loading…");

  useEffect(() => {
    loadOptions().then((value) => {
      setSettings(value);
      setStatus("");
    });
  }, []);

  if (!settings) {
    return <main className="page-shell"><p>{status}</p></main>;
  }

  const update = (patch: Partial<UserSettings>) => setSettings({ ...settings, ...patch });

  return (
    <main className="page-shell wide">
      <header className="page-header">
        <div>
          <h1>WebShield options</h1>
          <p className="muted">Configure detectors, actions, thresholds, preferences, and domain rules.</p>
        </div>
        <div className="actions-row">
          <button
            className="secondary"
            onClick={() =>
              resetOptions().then((value) => {
                setSettings(value);
                setStatus("Defaults restored.");
              })
            }
          >
            Reset
          </button>
          <button
            onClick={() =>
              saveOptions(settings).then((value) => {
                setSettings(value);
                setStatus("Settings saved.");
              })
            }
          >
            Save
          </button>
        </div>
      </header>

      <p className="muted">{status}</p>

      <HistorySettings
        history_enabled={settings.history_enabled}
        enabled={settings.enabled}
        onHistoryChange={(history_enabled) => update({ history_enabled })}
        onEnabledChange={(enabled) => update({ enabled })}
      />

      <DetectionSettings
        detectors={settings.detectors}
        scan_on_load={settings.scan_on_load}
        onScanOnLoadChange={(scan_on_load) => update({ scan_on_load })}
        onToggle={(key, value) =>
          update({
            detectors: {
              ...settings.detectors,
              [key]: value
            }
          })
        }
      />

      <ChildSafeMode value={settings.child_safe_mode} onChange={(child_safe_mode) => update({ child_safe_mode })} />

      <ActionSettings
        settings={settings}
        onThresholdChange={(category, value) =>
          update({
            thresholds: {
              ...settings.thresholds,
              [category]: value
            }
          })
        }
        onActionChange={(category, value: ActionType) =>
          update({
            category_actions: {
              ...settings.category_actions,
              [category]: value
            }
          })
        }
      />

      <PreferenceSettings interests={settings.interests} onChange={(interests) => update({ interests })} />

      <DomainRules
        allowlist={settings.allowlist}
        blocklist={settings.blocklist}
        onAllowlistChange={(allowlist) => update({ allowlist })}
        onBlocklistChange={(blocklist) => update({ blocklist })}
      />
    </main>
  );
}
