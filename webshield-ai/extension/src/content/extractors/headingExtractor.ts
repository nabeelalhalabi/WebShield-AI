import type { ExtractedHeadingItem } from "../../shared/types/page";
import { ensureElementId } from "../utils/elementIds";
import { getNormalizedText } from "../utils/dom";
import { collectHeadingElements } from "../scanner/elementCollector";

export function extractHeadingItems(limit = 10): ExtractedHeadingItem[] {
  return collectHeadingElements()
    .slice(0, limit)
    .map((element) => ({
      item_id: ensureElementId(element, "heading"),
      text: getNormalizedText(element),
      level: Number(element.tagName.toLowerCase().replace("h", "")) || 1,
      page_url: location.href,
      meta: {}
    }));
}
