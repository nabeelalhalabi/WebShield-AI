export const TEXT_SELECTORS = [
  "article p",
  "main p",
  "[role='main'] p",
  "section p",
  "article li",
  "main li",
  "[role='main'] li",
  "blockquote",
  "h1",
  "h2",
  "h3",
  "h4"
];

export const PROMO_SELECTORS = [
  "button",
  "a[role='button']",
  "[class*='promo']",
  "[class*='offer']",
  "[data-testid*='promo']",
  "[data-testid*='offer']"
];

export const IGNORE_SELECTORS = [
  "script",
  "style",
  "noscript",
  "code",
  "pre",
  "svg",
  "canvas",
  "nav",
  "footer",
  "header",
  "aside",
  "[aria-hidden='true']"
];

export const HEADING_SELECTORS = ["h1", "h2", "h3"];