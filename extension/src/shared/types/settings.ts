export type ActionType = "allow" | "warn" | "blur" | "hide" | "replace" | "block";

export interface DetectorToggles {
  toxicity: boolean;
  profanity: boolean;
  hate_speech: boolean;
  nsfw: boolean;
  violence: boolean;
  promotions: boolean;
  preference_match: boolean;
  explanations: boolean;
}

export interface UserSettings {
  enabled: boolean;
  child_safe_mode: boolean;
  scan_on_load: boolean;
  history_enabled: boolean;
  interests: string[];
  detectors: DetectorToggles;
  thresholds: Record<string, number>;
  category_actions: Record<string, ActionType>;
  allowlist: string[];
  blocklist: string[];
  max_text_items: number;
  max_image_items: number;
  max_promo_items: number;
}
