# Extension architecture

The extension uses Manifest V3 with:

- a background service worker for API communication and tab state
- a content script for scanning pages and applying DOM actions
- React pages for popup, options, and history screens

The content script never stores sensitive settings on its own. It reads them through shared storage helpers and sends analysis requests through the background worker.
