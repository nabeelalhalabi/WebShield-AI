from io import BytesIO
from typing import BinaryIO

from PIL import Image


def load_image_from_bytes(data: bytes) -> Image.Image:
    image = Image.open(BytesIO(data))
    if image.mode != "RGB":
        image = image.convert("RGB")
    return image


def thumbnail_copy(image: Image.Image, size: tuple[int, int] = (224, 224)) -> Image.Image:
    clone = image.copy()
    clone.thumbnail(size)
    return clone
