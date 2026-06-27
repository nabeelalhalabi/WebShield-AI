from io import BytesIO
from pathlib import Path

from PIL import Image

from app.config.settings import get_settings
from app.infrastructure.model_providers.nsfw_provider import NsfwProvider
from app.infrastructure.model_providers.violence_provider import ViolenceProvider

def main() -> None:
    settings = get_settings()
    nsfw = NsfwProvider(settings)
    violence = ViolenceProvider(settings)

    image = Image.new("RGB", (224, 224), color=(200, 200, 200))
    print("nsfw:", nsfw.predict(image))
    print("violence:", violence.predict(image))

if __name__ == "__main__":
    main()
