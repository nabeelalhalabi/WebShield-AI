export function applyHide(element: HTMLElement): void {
  if (!element.dataset.webshieldOriginalDisplay) {
    element.dataset.webshieldOriginalDisplay = element.style.display || "";
  }
  element.dataset.webshieldManaged = "true";
  element.style.display = "none";
}
