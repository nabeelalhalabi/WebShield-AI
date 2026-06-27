export function applyBlur(element: HTMLElement): void {
  if (!element.dataset.webshieldOriginalFilter) {
    element.dataset.webshieldOriginalFilter = element.style.filter || "";
  }
  if (!element.dataset.webshieldOriginalUserSelect) {
    element.dataset.webshieldOriginalUserSelect = element.style.userSelect || "";
  }
  element.dataset.webshieldManaged = "true";
  element.style.filter = "blur(10px)";
  element.style.userSelect = "none";
}
