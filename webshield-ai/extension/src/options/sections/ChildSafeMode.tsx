interface Props {
  value: boolean;
  onChange: (value: boolean) => void;
}

export function ChildSafeMode({ value, onChange }: Props) {
  return (
    <section className="card">
      <h2>Child-safe mode</h2>
      <label className="checkbox-row">
        <input type="checkbox" checked={value} onChange={(event) => onChange(event.target.checked)} />
        <span>Escalate harmful decisions to stricter actions</span>
      </label>
    </section>
  );
}
