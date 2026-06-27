export function applyReplace(element: HTMLElement): void {
  if (!element.dataset.webshieldOriginalHtml) {
    element.dataset.webshieldOriginalHtml = element.innerHTML;
  }
  element.dataset.webshieldManaged = "true";
  element.innerHTML = `<span class="webshield-replaced">[Filtered by WebShield]</span>`;
}
