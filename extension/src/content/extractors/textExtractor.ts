import type { ExtractedTextItem } from "../../shared/types/page";
import { ensureElementId } from "../utils/elementIds";
import { getNormalizedText } from "../utils/dom";
import { collectTextElements } from "../scanner/elementCollector";

export function extractTextItems(limit: number): ExtractedTextItem[] {
  return collectTextElements()
    .slice(0, limit)
    .map((element) => ({
      item_id: ensureElementId(element, "text"),
      text: getNormalizedText(element),
      tag_name: element.tagName.toLowerCase(),
      page_url: location.href,
      meta: {
        class_name: element.className || "",
        text_length: getNormalizedText(element).length
      }
    }));
}
