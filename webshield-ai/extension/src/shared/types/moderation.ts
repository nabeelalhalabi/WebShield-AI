import type { UserSettings } from "./settings";

export interface ModuleSignal {
  category: string;
  label: string;
  confidence: number;
  risk_level: number;
  reason: string;
  matched_rules: string[];
  raw_scores: Record<string, number>;
  model_name?: string | null;
  provider_status: string;
}

export interface ContentDecision {
  item_id: string;
  content_kind: string;
  action: "allow" | "warn" | "blur" | "hide" | "replace" | "block";
  risk_level: number;
  confidence: number;
  explanation: string;
  categories: string[];
  primary_category?: string | null;
  module_results: ModuleSignal[];
  meta: Record<string, unknown>;
}

export interface PreferenceMatch {
  score: number;
  top_interests: string[];
  compared_text: string;
}

export interface PageSummary {
  url: string;
  title: string;
  status: "safe" | "warning" | "restricted" | "blocked";
  safety_score: number;
  preference_match: PreferenceMatch;
  flagged_items: number;
  explanation: string;
  created_at: string;
}

export interface PageAnalysis {
  summary: PageSummary;
  items: unknown[];
  decisions: ContentDecision[];
  allowlisted: boolean;
  blocklisted: boolean;
  domain: string;
  meta: Record<string, unknown>;
}

export interface PageAnalysisRequest {
  url: string;
  title: string;
  text_items: Array<Record<string, unknown>>;
  image_items: Array<Record<string, unknown>>;
  promo_items: Array<Record<string, unknown>>;
  headings: Array<Record<string, unknown>>;
  preferences?: UserSettings;
}

export interface PageAnalysisResponse {
  analysis: PageAnalysis;
}
