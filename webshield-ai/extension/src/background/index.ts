import { handleMessage } from "./messageRouter";
import { forgetTabAnalysis } from "./tabStateManager";

chrome.runtime.onInstalled.addListener(() => {
  console.info("[WebShield] Extension installed.");
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  handleMessage(message, sender).then(sendResponse);
  return true;
});

chrome.tabs.onRemoved.addListener(async (tabId) => {
  await forgetTabAnalysis(tabId);
});
