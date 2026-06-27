import { DEFAULT_SETTINGS } from "../constants/defaults";
import type { UserSettings } from "../types/settings";
import { storageGet, storageSet } from "./chromeStorage";

const SETTINGS_KEY = "webshield.settings";

export async function loadSettings(): Promise<UserSettings> {
  const existing = await storageGet<UserSettings>(SETTINGS_KEY, "sync");
  return existing ?? DEFAULT_SETTINGS;
}

export async function saveSettings(settings: UserSettings): Promise<UserSettings> {
  await storageSet({ [SETTINGS_KEY]: settings }, "sync");
  return settings;
}
