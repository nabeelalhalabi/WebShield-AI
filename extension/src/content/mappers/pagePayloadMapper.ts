import type { PageAnalysisRequest } from "../../shared/types/moderation";
import type { ExtractedPage } from "../../shared/types/page";
import type { UserSettings } from "../../shared/types/settings";

export function toPageAnalysisRequest(page: ExtractedPage, settings: UserSettings): PageAnalysisRequest {
  return {
    url: page.url,
    title: page.title,
    text_items: page.text_items,
    image_items: page.image_items,
    promo_items: page.promo_items,
    headings: page.headings,
    preferences: settings
  };
}
