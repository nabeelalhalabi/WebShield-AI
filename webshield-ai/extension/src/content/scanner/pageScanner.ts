import type { ExtractedPage } from "../../shared/types/page";
import type { UserSettings } from "../../shared/types/settings";
import { extractHeadingItems } from "../extractors/headingExtractor";
import { extractImageItems } from "../extractors/imageExtractor";
import { extractPromoItems } from "../extractors/promoExtractor";
import { extractTextItems } from "../extractors/textExtractor";

export function scanPage(settings: UserSettings): ExtractedPage {
  return {
    url: location.href,
    title: document.title || location.href,
    text_items: extractTextItems(settings.max_text_items),
    image_items: extractImageItems(settings.max_image_items),
    promo_items: extractPromoItems(settings.max_promo_items),
    headings: extractHeadingItems()
  };
}
