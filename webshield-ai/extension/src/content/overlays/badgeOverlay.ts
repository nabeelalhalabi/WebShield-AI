export function attachBadge(element: HTMLElement, text: string): void {
  if (element.querySelector(":scope > .webshield-badge")) {
    return;
  }
  if (window.getComputedStyle(element).position === "static") {
    element.style.position = "relative";
  }

  const badge = document.createElement("span");
  badge.className = "webshield-badge";
  badge.textContent = text;
  element.appendChild(badge);
}
