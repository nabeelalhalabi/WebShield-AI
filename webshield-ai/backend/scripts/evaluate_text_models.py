from app.config.settings import get_settings
from app.infrastructure.model_providers.text_toxicity_provider import TextToxicityProvider
from app.infrastructure.model_providers.hate_speech_provider import HateSpeechProvider

SAMPLES = [
    "You are horrible and disgusting.",
    "I hope you have a wonderful day.",
    "Win a free phone right now by clicking here!",
]

def main() -> None:
    settings = get_settings()
    toxicity = TextToxicityProvider(settings)
    hate = HateSpeechProvider(settings)
    for sample in SAMPLES:
        print("=" * 80)
        print(sample)
        print("toxicity:", toxicity.predict(sample))
        print("hate:", hate.predict(sample))

if __name__ == "__main__":
    main()
