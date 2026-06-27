import overlayCss from "../styles/overlay.css?raw";
import { MESSAGES } from "../shared/constants/messages";
import type { PageAnalysis } from "../shared/types/moderation";
import { loadSettings } from "../shared/storage/localSettings";
import { logDebug, logError } from "../shared/utils/logger";
import { applyBlur } from "./actions/blurAction";
import { applyHide } from "./actions/hideAction";
import { applyReplace } from "./actions/replaceAction";
import { restoreManagedNodes } from "./actions/restoreAction";
import { applyWarn } from "./actions/warnAction";
import { toDecisionInstructions } from "./mappers/decisionMapper";
import { toPageAnalysisRequest } from "./mappers/pagePayloadMapper";
import { renderExplanationPanel } from "./overlays/explanationPanel";
import { attachBadge } from "./overlays/badgeOverlay";
import { renderPageBanner } from "./overlays/warningOverlay";
import { scanPage } from "./scanner/pageScanner";
import { findElementById } from "./utils/elementIds";

let lastUrl = location.href;
let initialized = false;
let mutationObserver: MutationObserver | null = null;
let rescanTimer: number | null = null;
let analysisRunning = false;

function injectOverlayStyles(): void {
  if (document.getElementById("webshield-overlay-styles")) return;

  const style = document.createElement("style");
  style.id = "webshield-overlay-styles";
  style.textContent = overlayCss;
  document.documentElement.appendChild(style);
}

function scheduleRescan(reason: "initial" | "manual" = "initial", delay = 800): void {
  if (rescanTimer !== null) {
    window.clearTimeout(rescanTimer);
  }

  rescanTimer = window.setTimeout(() => {
    runAnalysis(reason).catch(logError);
    rescanTimer = null;
  }, delay);
}

function applyAnalysis(analysis: PageAnalysis): void {
  restoreManagedNodes();

  const instructions = toDecisionInstructions(analysis.decisions);

  for (const instruction of instructions) {
    if (instruction.action === "allow") continue;

    const element = findElementById(instruction.itemId);
    if (!element) continue;

    switch (instruction.action) {
      case "warn":
        applyWarn(element);
        attachBadge(element, instruction.category || "warning");
        break;
      case "blur":
        applyBlur(element);
        attachBadge(element, instruction.category || "blurred");
        break;
      case "hide":
        applyHide(element);
        break;
      case "replace":
        applyReplace(element);
        attachBadge(element, instruction.category || "replaced");
        break;
      case "block":
        applyHide(element);
        break;
      default:
        break;
    }
  }

  renderPageBanner(analysis);
  renderExplanationPanel(analysis);
}

async function runAnalysis(reason: "initial" | "manual" = "initial"): Promise<void> {
  if (analysisRunning) return;
  analysisRunning = true;

  injectOverlayStyles();

  try {
    const settings = await loadSettings();

    if (!settings.enabled) {
      restoreManagedNodes();
      return;
    }

    if (reason === "initial" && !settings.scan_on_load) {
      return;
    }

    const page = scanPage(settings);
    const request = toPageAnalysisRequest(page, settings);

    const response = await chrome.runtime.sendMessage({
      type: MESSAGES.ANALYZE_PAGE,
      payload: { request }
    });

    if (!response?.ok) {
      throw new Error(response?.error || "Page analysis failed.");
    }

    applyAnalysis(response.data as PageAnalysis);
  } catch (error) {
    logError("Analysis failed", error);
  } finally {
    analysisRunning = false;
  }
}

function monitorUrlChanges(): void {
  setInterval(() => {
    if (location.href !== lastUrl) {
      lastUrl = location.href;
      scheduleRescan("initial", 1000);
    }
  }, 1000);
}

function isWebShieldNode(node: Node | null): boolean {
  if (!(node instanceof Element)) return false;

  return (
    node.id === "webshield-warning-banner" ||
    node.id === "webshield-explanation-panel" ||
    node.id === "webshield-overlay-styles" ||
    node.hasAttribute("data-webshield-managed") ||
    node.classList.contains("webshield-badge") ||
    node.classList.contains("webshield-warning-banner") ||
    node.classList.contains("webshield-explanation-panel")
  );
}

function shouldIgnoreMutationTarget(target: Node | null): boolean {
  if (!(target instanceof Element)) return false;

  return (
    isWebShieldNode(target) ||
    Boolean(
      target.closest(
        "#webshield-warning-banner, #webshield-explanation-panel, .webshield-badge, [data-webshield-managed='true']"
      )
    )
  );
}

function monitorDomChanges(): void {
  if (mutationObserver) return;

  mutationObserver = new MutationObserver((mutations) => {
    for (const mutation of mutations) {
      if (shouldIgnoreMutationTarget(mutation.target)) {
        continue;
      }

      if (mutation.type === "childList") {
        const addedRelevant = Array.from(mutation.addedNodes).some((node) => !isWebShieldNode(node));
        const removedRelevant = Array.from(mutation.removedNodes).some((node) => !isWebShieldNode(node));

        if (addedRelevant || removedRelevant) {
          scheduleRescan("initial", 1500);
          return;
        }
      }

      if (mutation.type === "attributes") {
        const target = mutation.target as Element;

        if (
          target instanceof HTMLImageElement ||
          target.matches("img, article, main, section, p, li, blockquote, h1, h2, h3, h4")
        ) {
          scheduleRescan("initial", 1500);
          return;
        }
      }
    }
  });

  mutationObserver.observe(document.documentElement, {
    childList: true,
    subtree: true,
    attributes: true,
    attributeFilter: ["src", "srcset"]
  });
}

function init(): void {
  if (initialized) return;
  initialized = true;

  runAnalysis("initial").catch(logError);

  window.setTimeout(() => scheduleRescan("initial", 1200), 1200);
  window.setTimeout(() => scheduleRescan("initial", 2500), 2500);

  monitorUrlChanges();
  monitorDomChanges();
}

chrome.runtime.onMessage.addListener((message) => {
  if (message.type === MESSAGES.RESCAN_PAGE) {
    scheduleRescan("manual", 100);
  }

  if (message.type === MESSAGES.RESTORE_PAGE) {
    restoreManagedNodes();
  }
});

window.addEventListener("load", init);

if (document.readyState === "complete" || document.readyState === "interactive") {
  init();
}

logDebug("WebShield content script loaded.");