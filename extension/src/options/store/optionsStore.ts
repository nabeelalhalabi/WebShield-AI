import { DEFAULT_SETTINGS } from "../../shared/constants/defaults";
import type { UserSettings } from "../../shared/types/settings";
import { loadSettings, saveSettings } from "../../shared/storage/localSettings";

export async function loadOptions(): Promise<UserSettings> {
  return loadSettings();
}

export async function saveOptions(settings: UserSettings): Promise<UserSettings> {
  return saveSettings(settings);
}

export async function resetOptions(): Promise<UserSettings> {
  return saveSettings(DEFAULT_SETTINGS);
}
