const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const controller = new AbortController();
  const timeoutMs = 90000;
  const timeout = globalThis.setTimeout(() => controller.abort("Request timeout"), timeoutMs);

  try {
    const response = await fetch(API_BASE_URL + path, {
      ...init,
      signal: controller.signal,
      headers: {
        "Content-Type": "application/json",
        ...(init?.headers ?? {})
      }
    });

    if (!response.ok) {
      const message = await response.text();
      throw new Error(message || `Request failed with status ${response.status}`);
    }

    return (await response.json()) as T;
  } catch (error) {
    if (error instanceof DOMException && error.name === "AbortError") {
      throw new Error(`Request timed out after ${timeoutMs / 1000} seconds.`);
    }
    throw error;
  } finally {
    globalThis.clearTimeout(timeout);
  }
}

export async function getJson<T>(path: string): Promise<T> {
  return request<T>(path, { method: "GET" });
}

export async function postJson<T>(path: string, body: unknown): Promise<T> {
  return request<T>(path, { method: "POST", body: JSON.stringify(body) });
}

export async function putJson<T>(path: string, body: unknown): Promise<T> {
  return request<T>(path, { method: "PUT", body: JSON.stringify(body) });
}

export async function deleteJson<T>(path: string): Promise<T> {
  return request<T>(path, { method: "DELETE" });
}