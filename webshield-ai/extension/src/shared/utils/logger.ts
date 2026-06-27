export function logDebug(...args: unknown[]): void {
  console.debug("[WebShield]", ...args);
}

export function logError(...args: unknown[]): void {
  console.error("[WebShield]", ...args);
}
