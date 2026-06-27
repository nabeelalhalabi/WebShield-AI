import { describe, expect, it } from "vitest";

import { toPageAnalysisRequest } from "../../src/content/mappers/pagePayloadMapper";
import { samplePage, sampleSettings } from "../fixtures/samplePage";

describe("page payload mapper", () => {
  it("builds the backend request shape", () => {
    const payload = toPageAnalysisRequest(samplePage, sampleSettings);
    expect(payload.url).toBe(samplePage.url);
    expect(payload.text_items).toHaveLength(1);
    expect(payload.promo_items).toHaveLength(1);
    expect(payload.preferences?.enabled).toBe(true);
  });
});
