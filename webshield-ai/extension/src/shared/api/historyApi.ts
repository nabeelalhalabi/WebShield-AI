import { deleteJson, getJson } from "./client";

export async function listHistory(limit = 50): Promise<{ items: Array<Record<string, unknown>> }> {
  return getJson(`/api/v1/history?limit=${limit}`);
}

export async function clearHistory(): Promise<{ status: string }> {
  return deleteJson("/api/v1/history");
}
