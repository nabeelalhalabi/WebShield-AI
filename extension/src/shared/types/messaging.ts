import type { PageAnalysis, PageAnalysisRequest } from "./moderation";
import type { UserSettings } from "./settings";

export type MessageType =
  | "ANALYZE_PAGE"
  | "GET_TAB_ANALYSIS"
  | "RESCAN_PAGE"
  | "RESCAN_ACTIVE_TAB"
  | "RESTORE_PAGE"
  | "RESTORE_ACTIVE_TAB"
  | "GET_SETTINGS"
  | "SAVE_SETTINGS"
  | "OPEN_OPTIONS"
  | "OPEN_HISTORY";

export interface RuntimeMessage<TPayload = unknown> {
  type: MessageType;
  payload?: TPayload;
}

export interface AnalyzePageMessagePayload {
  request: PageAnalysisRequest;
}

export interface SaveSettingsMessagePayload {
  settings: UserSettings;
}

export interface RuntimeResponse<TData = unknown> {
  ok: boolean;
  data?: TData;
  error?: string;
}

export interface TabAnalysisPayload {
  tabId?: number;
}

export interface SaveSettingsResponse {
  settings: UserSettings;
}

export interface AnalyzePageResponse {
  analysis: PageAnalysis;
}
