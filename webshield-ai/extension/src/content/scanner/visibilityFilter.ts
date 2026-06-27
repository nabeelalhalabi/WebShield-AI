import { getNormalizedText, isElementVisible, isIgnored } from "../utils/dom";

function hasBadImageHint(element: HTMLImageElement): boolean {
  const combined = `${element.className || ""} ${element.id || ""} ${element.alt || ""}`.toLowerCase();

  const blockedHints = [
    "logo",
    "icon",
    "avatar",
    "emoji",
    "sprite",
    "badge",
    "placeholder",
    "profile"
  ];

  return blockedHints.some((hint) => combined.includes(hint));
}

function isInsideIgnoredLayout(element: Element): boolean {
  return Boolean(element.closest("header, nav, footer, aside"));
}

function isLikelyDecorative(element: HTMLImageElement): boolean {
  const role = (element.getAttribute("role") || "").toLowerCase();
  const ariaHidden = (element.getAttribute("aria-hidden") || "").toLowerCase();

  if (role === "presentation") return true;
  if (ariaHidden === "true") return true;

  return false;
}

export function isUsefulTextElement(element: Element): boolean {
  const text = getNormalizedText(element);
  return !isIgnored(element) && isElementVisible(element) && text.length >= 20;
}

export function isUsefulImageElement(element: HTMLImageElement): boolean {
  const src = element.currentSrc || element.src || "";

  if (!isElementVisible(element)) return false;
  if (!src) return false;
  if (isInsideIgnoredLayout(element)) return false;
  if (hasBadImageHint(element)) return false;
  if (isLikelyDecorative(element)) return false;

  const width = element.naturalWidth || element.width || 0;
  const height = element.naturalHeight || element.height || 0;

  if (width < 140 || height < 140) return false;
  if (width * height < 35000) return false;

  return true;
}