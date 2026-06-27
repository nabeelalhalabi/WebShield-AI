import { IGNORE_SELECTORS } from "./selectors";

export function isElementVisible(element: Element): boolean {
  const html = element as HTMLElement;
  const style = window.getComputedStyle(html);
  const rect = html.getBoundingClientRect();

  return (
    style.display !== "none" &&
    style.visibility !== "hidden" &&
    Number(style.opacity) !== 0 &&
    rect.width > 8 &&
    rect.height > 8
  );
}

export function isIgnored(element: Element): boolean {
  return IGNORE_SELECTORS.some((selector) => element.matches(selector) || element.closest(selector));
}

export function getNormalizedText(element: Element): string {
  return (element.textContent || "").replace(/\s+/g, " ").trim();
}

export function getClassName(element: Element): string {
  return (element as HTMLElement).className || "";
}
