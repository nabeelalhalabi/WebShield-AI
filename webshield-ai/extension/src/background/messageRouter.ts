import { MESSAGES } from "../shared/constants/messages";
import { analyzePage } from "../shared/api/moderationApi";
import { loadSettings, saveSettings } from "../shared/storage/localSettings";
import type {
  AnalyzePageMessagePayload,
  RuntimeMessage,
  RuntimeResponse,
  SaveSettingsMessagePayload,
  TabAnalysisPayload
} from "../shared/types/messaging";
import { logError } from "../shared/utils/logger";
import { forgetTabAnalysis, readTabAnalysis, rememberTabAnalysis } from "./tabStateManager";

async function getActiveTabId(): Promise<number | undefined> {
  const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
  return tabs[0]?.id;
}

export async function handleMessage(
  message: RuntimeMessage,
  sender: chrome.runtime.MessageSender
): Promise<RuntimeResponse> {
  try {
    switch (message.type) {
      case MESSAGES.ANALYZE_PAGE: {
        const payload = message.payload as AnalyzePageMessagePayload;
        const response = await analyzePage(payload.request);
        const tabId = sender.tab?.id;
        if (typeof tabId === "number") {
          await rememberTabAnalysis(tabId, response.analysis);
        }
        return { ok: true, data: response.analysis };
      }

      case MESSAGES.GET_TAB_ANALYSIS: {
        const payload = (message.payload as TabAnalysisPayload | undefined) ?? {};
        const tabId = payload.tabId ?? sender.tab?.id ?? (await getActiveTabId());
        if (typeof tabId !== "number") {
          return { ok: true, data: null };
        }
        const analysis = await readTabAnalysis(tabId);
        return { ok: true, data: analysis ?? null };
      }

      case MESSAGES.RESCAN_ACTIVE_TAB: {
        const tabId = await getActiveTabId();
        if (typeof tabId === "number") {
          await chrome.tabs.sendMessage(tabId, { type: MESSAGES.RESCAN_PAGE });
        }
        return { ok: true };
      }

      case MESSAGES.RESTORE_ACTIVE_TAB: {
        const tabId = await getActiveTabId();
        if (typeof tabId === "number") {
          await chrome.tabs.sendMessage(tabId, { type: MESSAGES.RESTORE_PAGE });
          await forgetTabAnalysis(tabId);
        }
        return { ok: true };
      }

      case MESSAGES.GET_SETTINGS: {
        const settings = await loadSettings();
        return { ok: true, data: settings };
      }

      case MESSAGES.SAVE_SETTINGS: {
        const payload = message.payload as SaveSettingsMessagePayload;
        const settings = await saveSettings(payload.settings);
        return { ok: true, data: settings };
      }

      case MESSAGES.OPEN_OPTIONS: {
        await chrome.runtime.openOptionsPage();
        return { ok: true };
      }

      case MESSAGES.OPEN_HISTORY: {
        await chrome.tabs.create({ url: chrome.runtime.getURL("history/index.html") });
        return { ok: true };
      }

      default:
        return { ok: false, error: `Unsupported message type: ${message.type}` };
    }
  } catch (error) {
    logError("Background message error", error);
    return { ok: false, error: error instanceof Error ? error.message : "Unknown error" };
  }
}
