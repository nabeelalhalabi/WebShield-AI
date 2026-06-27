export function restoreManagedNodes(): void {
  const elements = Array.from(document.querySelectorAll<HTMLElement>("[data-webshield-managed='true']"));
  for (const element of elements) {
    if (element.dataset.webshieldOriginalDisplay !== undefined) {
      element.style.display = element.dataset.webshieldOriginalDisplay;
    }
    if (element.dataset.webshieldOriginalFilter !== undefined) {
      element.style.filter = element.dataset.webshieldOriginalFilter;
    }
    if (element.dataset.webshieldOriginalUserSelect !== undefined) {
      element.style.userSelect = element.dataset.webshieldOriginalUserSelect;
    }
    if (element.dataset.webshieldOriginalOutline !== undefined) {
      element.style.outline = element.dataset.webshieldOriginalOutline;
    }
    if (element.dataset.webshieldOriginalPosition !== undefined) {
      element.style.position = element.dataset.webshieldOriginalPosition;
    }
    if (element.dataset.webshieldOriginalHtml !== undefined) {
      element.innerHTML = element.dataset.webshieldOriginalHtml;
    }
    delete element.dataset.webshieldManaged;
  }

  document.querySelectorAll(".webshield-badge").forEach((node) => node.remove());
  document.querySelectorAll(".webshield-warning-banner").forEach((node) => node.remove());
  document.querySelectorAll(".webshield-explanation-panel").forEach((node) => node.remove());
}
