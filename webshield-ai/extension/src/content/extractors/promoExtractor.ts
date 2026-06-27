import type { ExtractedPromoItem } from "../../shared/types/page";
import { ensureElementId } from "../utils/elementIds";
import { getClassName, getNormalizedText } from "../utils/dom";
import { collectPromoElements } from "../scanner/elementCollector";

export function extractPromoItems(limit: number): ExtractedPromoItem[] {
  return collectPromoElements()
    .slice(0, limit)
    .map((element) => ({
      item_id: ensureElementId(element, "promo"),
      text: getNormalizedText(element),
      tag_name: element.tagName.toLowerCase(),
      role: element.getAttribute("role") || undefined,
      class_name: getClassName(element),
      page_url: location.href,
      meta: {
        aria_label: element.getAttribute("aria-label") || ""
      }
    }));
}
