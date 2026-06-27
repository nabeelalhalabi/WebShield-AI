import type { PageAnalysis } from "../shared/types/moderation";
import { clearAnalysisForTab, getAnalysisForTab, setAnalysisForTab } from "../shared/storage/sessionState";

export async function rememberTabAnalysis(tabId: number, analysis: PageAnalysis): Promise<void> {
  await setAnalysisForTab(tabId, analysis);
}

export async function readTabAnalysis(tabId: number): Promise<PageAnalysis | undefined> {
  return getAnalysisForTab(tabId);
}

export async function forgetTabAnalysis(tabId: number): Promise<void> {
  await clearAnalysisForTab(tabId);
}
