from __future__ import annotations

import base64
from urllib.parse import unquote

import requests
from PIL import Image

from app.common.security.safe_url_checks import is_safe_web_url
from app.common.utils.image_processing import load_image_from_bytes
from app.config.settings import Settings


class ImageDownloader:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def fetch(self, source_url: str) -> Image.Image:
        if source_url.startswith("data:image"):
            _, encoded = source_url.split(",", 1)
            raw = base64.b64decode(unquote(encoded))
            return load_image_from_bytes(raw)

        if not is_safe_web_url(source_url):
            raise ValueError("Unsupported image source URL.")

        response = requests.get(
            source_url,
            timeout=self.settings.request_timeout_seconds,
            headers={"User-Agent": "WebShieldAI/0.1"},
        )
        response.raise_for_status()
        return load_image_from_bytes(response.content)
