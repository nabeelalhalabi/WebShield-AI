import type { PageAnalysisRequest, PageAnalysisResponse } from "../types/moderation";
import { getJson, postJson } from "./client";

export async function analyzePage(request: PageAnalysisRequest): Promise<PageAnalysisResponse> {
  return postJson<PageAnalysisResponse>("/api/v1/moderation/page", request);
}

export async function getHealth(): Promise<unknown> {
  return getJson("/api/v1/health");
}
