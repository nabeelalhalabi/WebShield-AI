import { describe, expect, it } from "vitest";

import { normalizeText, truncateText } from "../../src/shared/utils/text";

describe("text utils", () => {
  it("normalizes whitespace", () => {
    expect(normalizeText("hello\n\nworld")).toBe("hello world");
  });

  it("truncates long text", () => {
    expect(truncateText("a".repeat(200), 20).length).toBeLessThanOrEqual(20);
  });
});
