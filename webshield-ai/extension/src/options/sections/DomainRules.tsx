interface Props {
  allowlist: string[];
  blocklist: string[];
  onAllowlistChange: (values: string[]) => void;
  onBlocklistChange: (values: string[]) => void;
}

export function DomainRules({
  allowlist,
  blocklist,
  onAllowlistChange,
  onBlocklistChange
}: Props) {
  return (
    <section className="card">
      <h2>Domain rules</h2>
      <div className="two-column">
        <div>
          <label>Allowlist</label>
          <textarea
            rows={5}
            value={allowlist.join("\n")}
            onChange={(event) =>
              onAllowlistChange(
                event.target.value.split(/\n|,/).map((value) => value.trim()).filter(Boolean)
              )
            }
          />
        </div>
        <div>
          <label>Blocklist</label>
          <textarea
            rows={5}
            value={blocklist.join("\n")}
            onChange={(event) =>
              onBlocklistChange(
                event.target.value.split(/\n|,/).map((value) => value.trim()).filter(Boolean)
              )
            }
          />
        </div>
      </div>
    </section>
  );
}
