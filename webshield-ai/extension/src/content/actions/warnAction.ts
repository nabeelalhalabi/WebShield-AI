export function applyWarn(element: HTMLElement): void {
  if (!element.dataset.webshieldOriginalOutline) {
    element.dataset.webshieldOriginalOutline = element.style.outline || "";
  }
  if (!element.dataset.webshieldOriginalPosition) {
    element.dataset.webshieldOriginalPosition = element.style.position || "";
  }
  element.dataset.webshieldManaged = "true";
  if (window.getComputedStyle(element).position === "static") {
    element.style.position = "relative";
  }
  element.style.outline = "2px solid #f59e0b";
}
