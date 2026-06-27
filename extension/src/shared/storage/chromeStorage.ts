type StorageAreaName = "local" | "sync" | "session";

const memoryStorage = new Map<string, unknown>();

function hasChromeStorage(): boolean {
  return typeof chrome !== "undefined" && Boolean(chrome.storage);
}

function getArea(area: StorageAreaName): chrome.storage.StorageArea | null {
  if (!hasChromeStorage()) {
    return null;
  }
  return chrome.storage[area];
}

export async function storageGet<T>(key: string, area: StorageAreaName = "local"): Promise<T | undefined> {
  const storageArea = getArea(area);
  if (!storageArea) {
    return memoryStorage.get(key) as T | undefined;
  }
  const result = await storageArea.get(key);
  return result[key] as T | undefined;
}

export async function storageSet(value: Record<string, unknown>, area: StorageAreaName = "local"): Promise<void> {
  const storageArea = getArea(area);
  if (!storageArea) {
    Object.entries(value).forEach(([key, item]) => memoryStorage.set(key, item));
    return;
  }
  await storageArea.set(value);
}

export async function storageRemove(key: string, area: StorageAreaName = "local"): Promise<void> {
  const storageArea = getArea(area);
  if (!storageArea) {
    memoryStorage.delete(key);
    return;
  }
  await storageArea.remove(key);
}
