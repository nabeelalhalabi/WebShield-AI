import type { ExtractedImageItem } from "../../shared/types/page";
import { ensureElementId } from "../utils/elementIds";
import { collectImageElements } from "../scanner/elementCollector";

export function extractImageItems(limit: number): ExtractedImageItem[] {
  return collectImageElements()
    .slice(0, limit)
    .map((element) => ({
      item_id: ensureElementId(element, "image"),
      src: element.currentSrc || element.src,
      alt_text: element.alt || "",
      width: element.naturalWidth || element.width,
      height: element.naturalHeight || element.height,
      tag_name: element.tagName.toLowerCase(),
      page_url: location.href,
      meta: {
        class_name: element.className || ""
      }
    }));
}
