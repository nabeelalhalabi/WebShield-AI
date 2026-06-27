import type { PageAnalysis } from "../types/moderation";
import { storageGet, storageRemove, storageSet } from "./chromeStorage";

function keyForTab(tabId: number): string {
  return `webshield.tab.${tabId}`;
}

export async function setAnalysisForTab(tabId: number, analysis: PageAnalysis): Promise<void> {
  await storageSet({ [keyForTab(tabId)]: analysis }, "session");
}

export async function getAnalysisForTab(tabId: number): Promise<PageAnalysis | undefined> {
  return storageGet<PageAnalysis>(keyForTab(tabId), "session");
}

export async function clearAnalysisForTab(tabId: number): Promise<void> {
  await storageRemove(keyForTab(tabId), "session");
}
