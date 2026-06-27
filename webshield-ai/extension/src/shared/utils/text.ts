export function normalizeText(value: string): string {
  return value.replace(/\s+/g, " ").trim();
}

export function truncateText(value: string, maxLength = 120): string {
  const normalized = normalizeText(value);
  if (normalized.length <= maxLength) {
    return normalized;
  }
  return normalized.slice(0, maxLength - 1).trimEnd() + "…";
}
