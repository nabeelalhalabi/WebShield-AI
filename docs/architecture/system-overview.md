# System overview

WebShield AI is split into two runtime layers.

1. The browser extension extracts visible content from pages and applies DOM actions.
2. The backend API scores that content, runs pretrained models, fuses policy decisions, and returns explanations.

## Analysis pipeline

1. Content script extracts visible text blocks, images, headings, and promotion-like UI elements.
2. Background worker sends the payload to the backend API.
3. Backend detectors run toxicity, hate, profanity, NSFW, violence, and promotion checks.
4. Policy engine applies thresholds and user actions.
5. Safety score and preference match are computed.
6. Extension renders warn / blur / hide / replace decisions on the page.
