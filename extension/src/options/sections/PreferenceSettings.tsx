interface Props {
  interests: string[];
  onChange: (interests: string[]) => void;
}

export function PreferenceSettings({ interests, onChange }: Props) {
  return (
    <section className="card">
      <h2>Preference matching</h2>
      <textarea
        rows={5}
        value={interests.join("\n")}
        onChange={(event) =>
          onChange(
            event.target.value
              .split(/\n|,/)
              .map((value) => value.trim())
              .filter(Boolean)
          )
        }
        placeholder="One interest per line"
      />
    </section>
  );
}
