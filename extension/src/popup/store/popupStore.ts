import { MESSAGES } from "../../shared/constants/messages";
import type { PageAnalysis } from "../../shared/types/moderation";
import type { UserSettings } from "../../shared/types/settings";
import { loadSettings, saveSettings } from "../../shared/storage/localSettings";

async function getActiveTabId(): Promise<number | undefined> {
  const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
  return tabs[0]?.id;
}

export async function loadPopupState(): Promise<{ analysis: PageAnalysis | null; settings: UserSettings }> {
  const settings = await loadSettings();
  const tabId = await getActiveTabId();
  if (typeof tabId !== "number") {
    return { analysis: null, settings };
  }
  const response = await chrome.runtime.sendMessage({
    type: MESSAGES.GET_TAB_ANALYSIS,
    payload: { tabId }
  });
  return {
    analysis: (response?.data as PageAnalysis | null) ?? null,
    settings
  };
}

export async function toggleEnabled(settings: UserSettings): Promise<UserSettings> {
  const updated = { ...settings, enabled: !settings.enabled };
  await saveSettings(updated);
  if (updated.enabled) {
    await chrome.runtime.sendMessage({ type: MESSAGES.RESCAN_ACTIVE_TAB });
  } else {
    await chrome.runtime.sendMessage({ type: MESSAGES.RESTORE_ACTIVE_TAB });
  }
  return updated;
}

export async function rescanCurrentTab(): Promise<void> {
  await chrome.runtime.sendMessage({ type: MESSAGES.RESCAN_ACTIVE_TAB });
}

export async function restoreCurrentTab(): Promise<void> {
  await chrome.runtime.sendMessage({ type: MESSAGES.RESTORE_ACTIVE_TAB });
}

export async function openOptionsPage(): Promise<void> {
  await chrome.runtime.sendMessage({ type: MESSAGES.OPEN_OPTIONS });
}

export async function openHistoryPage(): Promise<void> {
  await chrome.runtime.sendMessage({ type: MESSAGES.OPEN_HISTORY });
}
