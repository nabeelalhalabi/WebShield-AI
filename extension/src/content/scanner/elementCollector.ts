import { HEADING_SELECTORS, PROMO_SELECTORS, TEXT_SELECTORS } from "../utils/selectors";
import { getNormalizedText, isIgnored } from "../utils/dom";
import { isUsefulImageElement, isUsefulTextElement } from "./visibilityFilter";

function uniqueByText<T extends Element>(elements: T[]): T[] {
  const seen = new Set<string>();
  const output: T[] = [];
  for (const element of elements) {
    const signature = getNormalizedText(element).slice(0, 160);
    if (!signature || seen.has(signature)) continue;
    seen.add(signature);
    output.push(element);
  }
  return output;
}

export function collectTextElements(): HTMLElement[] {
  const raw = Array.from(document.querySelectorAll<HTMLElement>(TEXT_SELECTORS.join(",")));
  const filtered = raw.filter((element) => isUsefulTextElement(element));
  return uniqueByText(filtered).slice(0, 200);
}

export function collectImageElements(): HTMLImageElement[] {
  const raw = Array.from(document.querySelectorAll<HTMLImageElement>("img"));
  return raw.filter((element) => isUsefulImageElement(element)).slice(0, 60);
}

export function collectPromoElements(): HTMLElement[] {
  const raw = Array.from(document.querySelectorAll<HTMLElement>(PROMO_SELECTORS.join(",")));
  const filtered = raw.filter((element) => !isIgnored(element) && getNormalizedText(element).length >= 6);
  return uniqueByText(filtered).slice(0, 80);
}

export function collectHeadingElements(): HTMLElement[] {
  const raw = Array.from(document.querySelectorAll<HTMLElement>(HEADING_SELECTORS.join(",")));
  return raw.filter((element) => !isIgnored(element) && getNormalizedText(element).length >= 3).slice(0, 20);
}
