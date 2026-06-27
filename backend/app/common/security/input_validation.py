from app.common.exceptions import ValidationError
from app.common.security.safe_url_checks import is_safe_web_url


def validate_counts(
    *,
    text_items: int,
    image_items: int,
    promo_items: int,
    max_text_items: int,
    max_image_items: int,
    max_promo_items: int,
) -> None:
    if text_items > max_text_items:
        raise ValidationError(f"text_items exceeds limit of {max_text_items}")
    if image_items > max_image_items:
        raise ValidationError(f"image_items exceeds limit of {max_image_items}")
    if promo_items > max_promo_items:
        raise ValidationError(f"promo_items exceeds limit of {max_promo_items}")


def validate_page_url(url: str) -> None:
    if url and not is_safe_web_url(url):
        raise ValidationError("Unsupported page URL scheme.")
