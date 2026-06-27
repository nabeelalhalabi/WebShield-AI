import type { ExtractedPage } from "../../src/shared/types/page";
import type { UserSettings } from "../../src/shared/types/settings";
import { DEFAULT_SETTINGS } from "../../src/shared/constants/defaults";

export const samplePage: ExtractedPage = {
  url: "https://example.com",
  title: "Cars article",
  text_items: [{ item_id: "t-1", text: "This is a car review.", tag_name: "p" }],
  image_items: [],
  promo_items: [{ item_id: "p-1", text: "YOU WON 100000 DOLLARS!!!", tag_name: "button" }],
  headings: [{ item_id: "h-1", text: "Electric cars", level: 1 }]
};

export const sampleSettings: UserSettings = DEFAULT_SETTINGS;
