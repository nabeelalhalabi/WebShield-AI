import type { UserSettings } from "../types/settings";
import { DEFAULT_THRESHOLDS } from "./thresholds";

export const DEFAULT_SETTINGS: UserSettings = {
  enabled: true,
  child_safe_mode: false,
  scan_on_load: true,
  history_enabled: true,
  interests: ["technology", "cars", "science"],
  detectors: {
    toxicity: true,
    profanity: true,
    hate_speech: true,
    nsfw: true,
    violence: true,
    promotions: true,
    preference_match: true,
    explanations: true
  },
  thresholds: DEFAULT_THRESHOLDS,
  category_actions: {
    toxicity: "warn",
    profanity: "warn",
    hate_speech: "hide",
    nsfw: "blur",
    violence: "blur",
    promotions: "warn"
  },
  allowlist: [],
  blocklist: [],
  max_text_items: 40,
  max_image_items: 12,
  max_promo_items: 12
};
