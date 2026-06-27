let counter = 0;

export function ensureElementId(element: Element, prefix = "ws"): string {
  const htmlElement = element as HTMLElement;
  const existing = htmlElement.dataset.webshieldId;
  if (existing) {
    return existing;
  }
  counter += 1;
  const id = `${prefix}-${Date.now().toString(36)}-${counter}`;
  htmlElement.dataset.webshieldId = id;
  return id;
}

export function findElementById(id: string): HTMLElement | null {
  const safeId = typeof CSS !== "undefined" && CSS.escape ? CSS.escape(id) : id;
  return document.querySelector(`[data-webshield-id="${safeId}"]`);
}
